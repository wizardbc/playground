import streamlit as st
import openai
from utils.streamlit import undo, stream_display
import functions
import json
from datetime import datetime

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

# OpenAI API key
if "api_key" not in st.session_state:
  try:
    st.session_state.api_key = st.secrets["OPENAI_API_KEY"]
  except:
    st.session_state.api_key = ""
    st.write("Your OpenAI API Key is not provided in `.streamlit/secrets.toml`, but you can input one in the sidebar for temporary use.")

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Sidebar for parameters
with st.sidebar:
  # OpenAI API Key
  if not st.session_state.api_key:
    st.header("OpenAI API Key")
    st.session_state.api_key = st.text_input("OpenAI API Key", type="password")
  else:
    openai.api_key = st.session_state.api_key

  # Role selection and Undo
  st.header("Chat")
  chat_role = st.selectbox("role", ["system", "assistant", "user", "function"], index=2)
  st.button("Undo", on_click=undo)

  st.subheader("Visible")
  system_checkbox = st.checkbox("system", value=True)
  f_call_checkbox = st.checkbox("function", value=True)
  
  # ChatCompletion parameters
  st.header("Parameters")
  chat_params = {
    "model": st.selectbox("model", ["gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-4-0613", "gpt-4-32k-0613"]),
    "n": st.number_input("n", min_value=1, value=1),
    "temperature": st.slider("temperature", min_value=0.0, max_value=2.0, value=1.0),
    "max_tokens": st.number_input("max_tokens", min_value=1, value=512),
    "top_p": st.slider("top_p", min_value=0.0, max_value=1.0, value=1.0),
    "presence_penalty": st.slider("presence_penalty", min_value=-2.0, max_value=2.0, value=0.0),
    "frequency_penalty": st.slider("frequency_penalty", min_value=-2.0, max_value=2.0, value=0.0),
    "stream": True,
  }

  # Functions
  st.header("Functions")
  func_checkbox = [st.checkbox(f.get("desc").get("name")) for f in functions.available]

  # Upload and Download
  st.header("Upload & Download Conversation")
  with st.form("Upload", clear_on_submit=True):
    uploaded_file = st.file_uploader(
      label="Choose a JSON file",
      accept_multiple_files=False,
      type='json'
    )
    submitted = st.form_submit_button("Upload")
    if (uploaded_file is not None) and submitted:
      st.session_state.messages = json.load(uploaded_file)
  st.download_button(
    label="Download the JSON file",
    data=json.dumps(st.session_state.messages),
    file_name=f'chat_history_{datetime.now().strftime("%Y%m%d%H%M%S")}.json',
    mime="application/json"
  )

# Display messages in history
roles = ["user", "assistant"]
if system_checkbox:
  roles.append("system")
if f_call_checkbox:
  roles.append("function")

for msg in st.session_state.messages:
  if (role := msg.get("role")) in roles:
    if content := msg.get("content", ""):
      with st.chat_message(role):
        st.write(content)
    if f_call_checkbox:
      if f_name := msg.get("function_call", {}).get("name", ""):
        f_args = msg.get("function_call").get("arguments", "")
        with st.chat_message(role):
          st.write(f"function_call: {f_name}(), args: {f_args}")

# In the case of the role of the last entry of the history is function
if st.session_state.messages:
  if st.session_state.messages[-1].get("role") == "function":
    # ChatCompletion
    response = openai.ChatCompletion.create(
      messages=st.session_state.messages,
      **chat_params
    )
    # Number of choices
    n = chat_params.get("n")
    # Stream display
    stream_display(response, n)

# Chat input
if prompt := st.chat_input():
  # User message
  user_msg = {
    "role": chat_role,
    "content": prompt,
  }
  # function role need name
  if chat_role == "function":
    user_msg.update({"name": "dummy"})
  # Display user message
  with st.chat_message(chat_role):
    st.write(prompt)
  # Append to history
  st.session_state.messages.append(user_msg)

  if chat_role == "user":
    # parameter `functions`
    func_desc = [functions.available[i].get("desc") for i, check in enumerate(func_checkbox) if check]
    if func_desc:
      chat_params["functions"] = func_desc
    else:
      chat_params.pop("functions", None)

    # ChatCompletion
    response = openai.ChatCompletion.create(
      messages=st.session_state.messages,
      **chat_params
    )
    # Number of choices
    n = chat_params.get("n")
    # Stream display
    stream_display(response, n)