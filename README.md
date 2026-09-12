# autogen_coding_agent
A minimal Streamlit application using AutoGen. An AssistantAgent writes a self-contained Python solution, and a UserProxyAgent executes it through code_execution_config, returns the real output, and continues the conversation until the coding agent explains the result.

_**Installation Steps:**_ <br>
**cd autogen_coding_agent** <br>
**python3 -m venv autoenv** <br>
**source autoenv/bin/activate** <br>
**pip install -r requirements.txt** <br>
**streamlit run app.py** <br>

# UI
In the UI you can pass your OPENROUTER key and select the model.
