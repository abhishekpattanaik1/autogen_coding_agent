# autogen_coding_agent
A minimal Streamlit application using AutoGen. An AssistantAgent writes a self-contained Python solution, and a UserProxyAgent executes it through code_execution_config, returns the real output, and continues the conversation until the coding agent explains the result.

# How to run the agent
cd autogen_coding_agent
python3 -m venv autoenv
source autoenv/bin/activate
pip install -r requirements.txt
streamlit run app.py

# UI
In the UI you can pass your OPENROUTER key and select the model.
