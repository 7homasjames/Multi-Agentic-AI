import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8000/agentic_workflow/"  

st.title("AI Insurance Risk Assessor")
st.markdown("Enter a policy number to analyze risk factors.")

# Input field for policy number
policy_number = st.text_input("Policy Number")

if st.button("Analyze Risk"):
    if not policy_number.strip():
        st.warning("Please enter a valid policy number.")
    else:
        with st.spinner("Generating response..."):
            response = requests.post(API_URL, json={"policy_number": policy_number})  # Send only policy_number
            if response.status_code == 200:
                #print(response.json().type)
                response_data = response.json() 
                final_response = response_data["output"]["chat_history"][5]["content"]
                print(final_response)
                output = response.json().get("output", "No response generated.")
                st.success("Response generated successfully!")
                st.chat_message("assistant").write(final_response)
                st.write(output)
                
            else:
                st.error(f"Error {response.status_code}: {response.text}")

