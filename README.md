# AI Insurance Risk Assessor

This project consists of a FastAPI backend and a Streamlit frontend designed to analyze insurance risk factors using AI-driven agents.

## Features

- **FastAPI Backend**: Handles insurance policy data and orchestrates agentic workflows for risk assessment.
- **Streamlit Frontend**: Provides a user-friendly interface to input policy numbers and view risk assessment results.
- **AI Agent Workflow**: Utilizes multiple AI agents to assess risks based on policyholder information.
- **Autogen Integration**: Leverages OpenAI-powered AI agents for decision-making.

![image](https://github.com/user-attachments/assets/68c76906-62da-497b-8f9c-fce21aaa0edf)

## Installation

### Prerequisites

- Python 3.8+
- `pip` package manager

### Setup

1. Clone this repository:

   ```sh
   git clone https://github.com/your-repo/ai-insurance-risk-assessor.git
   cd ai-insurance-risk-assessor
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```sh
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## Running the Application

### Start the FastAPI Backend

```sh
uvicorn api2:app --reload
```

### Start the Streamlit Frontend

```sh
streamlit run app.py
```

## API Endpoints

### `POST /agentic_workflow/`

- **Request Body:**
  ```json
  {
    "policy_number": "12345ABC"
  }
  ```
- **Response:**
  ```json
  {
    "output": "Risk assessment results..."
  }
  ```

## File Structure

```
📦 ai-insurance-risk-assessor
🕽️ api2.py        # FastAPI backend
🕽️ app.py         # Streamlit frontend
🕽️ requirements.txt  # Project dependencies
🕽️ insurance_profile.json  # Sample insurance data (ensure this file exists)
🕽️ README.md      # Project documentation
```

## Notes

- Make sure `insurance_profile.json` is present in the project directory.
- The FastAPI server should be running before launching the Streamlit app.
- Adjust `API_URL` in `app.py` if hosting the backend on a remote server.

## License

This project is licensed under the MIT License.

