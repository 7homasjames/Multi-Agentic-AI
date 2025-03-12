import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import autogen

app = FastAPI()


DATA_FILE = "insurance_profile.json"

try:
    with open(DATA_FILE, "r") as f:
        insurance_data = json.load(f)
except Exception as e:
    raise RuntimeError(f"Error loading insurance data: {e}")


llm_config = {
    "model": "gpt-3.5-turbo",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": 0.3
}

# Define Pydantic Request Model
class WorkflowRequest(BaseModel):
    policy_number: str


def get_insurance_profile(policy_number: str) -> Dict:
    """Fetches the insurance profile based on policy number from the JSON data."""
    for policy in insurance_data.get("policies", []):
        if policy["policy_number"] == policy_number:
            return policy["customer_profile"]
    return None  # Return None if policy not found


agents = [
    autogen.UserProxyAgent(
        name="underwriter_assessor",
        system_message="Assess risk factors based on the insurance profile.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
        llm_config=llm_config
    ),
    autogen.AssistantAgent(
        name="insurance_profiler_agent",
        system_message="Retrieve the insurance profile based on the policy number.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.ConversableAgent(
        name="general_medical_practitioner",
        system_message="Analyze underlying medical conditions.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.AssistantAgent(
        name="medical_expert",
        system_message="Provide a detailed risk analysis based on medical history.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.ConversableAgent(
        name="summary_agent",
        system_message="Summarize the medical risk analysis.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    ),
    autogen.AssistantAgent(
        name="guardrail_agent",
        system_message="Ensure ethical and responsible responses.",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        llm_config=llm_config
    )
]


agent_dict = {agent.name: agent for agent in agents}  # This ensures we have correct mappings


fsm_graph = {
    agent_dict["underwriter_assessor"]: [agent_dict["insurance_profiler_agent"]],
    agent_dict["insurance_profiler_agent"]: [agent_dict["general_medical_practitioner"]],
    agent_dict["general_medical_practitioner"]: [agent_dict["medical_expert"]],
    agent_dict["medical_expert"]: [agent_dict["summary_agent"]],
    agent_dict["summary_agent"]: [agent_dict["guardrail_agent"]],
    agent_dict["guardrail_agent"]: []  # No looping back
}


for key in fsm_graph.keys():
    if key not in agents:
        raise ValueError(f"FSM Graph Error: '{key.name}' is not a valid agent object.")


# Initialize Group Chat
groupchat = autogen.GroupChat(
    agents=agents,
    messages=[],
    allowed_or_disallowed_speaker_transitions=fsm_graph,
    speaker_transitions_type="allowed",
    send_introductions=True,
    func_call_filter=True,
    max_round=6  # Prevent infinite looping
)


manager = autogen.GroupChatManager(
    groupchat=groupchat,
    name="ChatManager",
    system_message="Managing agentic workflow.",
    human_input_mode="TERMINATE",
    llm_config=llm_config
)

@app.post("/agentic_workflow/")
async def agentic_workflow(request: WorkflowRequest):
    policy_number = request.policy_number.strip()
    
    # Fetch insurance profile from JSON
    insurance_profile = get_insurance_profile(policy_number)
    if not insurance_profile:
        raise HTTPException(status_code=404, detail="Insurance profile not found.")

    # Start the workflow with the first agent
    underwriter_assessor = next(a for a in agents if a.name == "underwriter_assessor")
    response = underwriter_assessor.initiate_chat(
        recipient=manager, 
        message=f"Process insurance profile for policy {policy_number}: {insurance_profile}"
    )

    return {"output": response.get("content", "No response generated.") if isinstance(response, dict) else response}
