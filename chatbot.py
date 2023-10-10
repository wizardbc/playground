import streamlit as st
import openai
from utils.streamlit import append_history
from utils.openai import Stream2Msgs

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

# OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display messages in history
for msg in st.session_state.messages:
  if content := msg.get("content", ""):
    with st.chat_message(msg.get("role")):
      st.write(content)

# Sidebar for parameters
with st.sidebar:
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

# Chat input
if prompt := st.chat_input("What is up?"):
  # User message
  user_msg = {
    "role": "user",
    "content": prompt,
  }
  # Display user message
  with st.chat_message("user"):
    st.write(prompt)
  # Append to history
  st.session_state.messages.append(user_msg)

  # ChatCompletion
  response = openai.ChatCompletion.create(
    messages=st.session_state.messages,
    **chat_params
  )
  # Number of choices
  n = chat_params.get("n")
  # To concatenate tokens in delta
  full_msgs = Stream2Msgs(n)
  # Placeholders
  with st.chat_message("assistant"):
    placeholders = [
      {
        "text": st.empty(),
        "button": st.button(
          f"Choose Answer No. {i+1}",
          on_click=append_history, args=[full_msgs, i]
        ) if n > 1 else None,
        "_divider": st.divider() if n > 1 else None,
      } for i in range(n)
    ]
  # Write delta on placeholders
  for res in response:
    i, msg = full_msgs(res)
    placeholders[i].get("text").write(msg.get("content") + "▌")
  # Write full message on placeholders
  for i in range(n):
    placeholders[i].get("text").write(full_msgs.msgs[i].get("content"))
  if n == 1:
    append_history(full_msgs, 0)