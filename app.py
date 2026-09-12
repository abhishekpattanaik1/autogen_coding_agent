"""
Minimal Streamlit + AutoGen (AG2 / pyautogen) coding assistant.

- AssistantAgent writes a self-contained Python solution to a task.
- UserProxyAgent executes that code locally (no Docker) and feeds the
  real stdout/stderr back to the AssistantAgent.
- The two agents keep talking until the AssistantAgent explains the
  result and says TERMINATE.
- The model is called through OpenRouter's OpenAI-compatible endpoint.

Run with:
    pip install -r requirements.txt
    streamlit run app.py
"""

import tempfile

import autogen
import streamlit as st

st.set_page_config(page_title="AutoGen Coding Assistant", page_icon="🤖")
st.title("🤖 AutoGen Coding Assistant (OpenRouter)")

# --- Sidebar: OpenRouter credentials -----------------------------------
with st.sidebar:
    st.header("OpenRouter settings")
    api_key = st.text_input("OpenRouter API key", type="password")
    model_name = st.text_input(
        "OpenRouter model",
        value="openai/gpt-4o-mini",
        help="Any OpenRouter model id, e.g. openai/gpt-4o-mini, "
             "anthropic/claude-3.5-sonnet, qwen/qwen-2.5-coder-32b-instruct",
    )
    st.caption(
        "The key is kept only in this browser session's memory "
        "(st.session_state) and is sent directly to OpenRouter — never "
        "stored on disk."
    )

st.warning(
    "This app executes the model's generated Python code locally on this "
    "machine (Docker is disabled for simplicity). Only run tasks you trust.",
    icon="⚠️",
)

# --- Main: task input ----------------------------------------------------
task = st.text_area(
    "Describe a small coding task",
    height=100,
    placeholder="e.g. Write a function that checks if a number is prime, "
                "then test it on 17 and 18.",
)

ready = bool(api_key and model_name and task)
run = st.button("Submit", type="primary", disabled=not ready)

if run:
    llm_config = {
        "config_list": [
            {
                "model": model_name,
                "api_key": api_key,
                "base_url": "https://openrouter.ai/api/v1",
            }
        ],
        "temperature": 0,
    }

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        system_message=(
            "You are a helpful AI coding assistant. For each task, write a "
            "complete, self-contained Python solution in a single code "
            "block so it can be executed as-is. Once you see the real "
            "execution result, briefly explain it in plain language, then "
            "end your final message with the word TERMINATE."
        ),
    )

    work_dir = tempfile.mkdtemp()
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
        code_execution_config={"work_dir": work_dir, "use_docker": False},
    )

    with st.spinner("Agents are working on it..."):
        try:
            user_proxy.initiate_chat(assistant, message=task)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Conversation")
    history = assistant.chat_messages.get(user_proxy, [])
    for msg in history:
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        role = "assistant" if msg.get("role") == "assistant" else "user"
        with st.chat_message(role):
            st.markdown(content)
