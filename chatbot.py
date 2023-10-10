import streamlit as st
import openai

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
    "n": 1,
    # "n": st.number_input("n", min_value=1, value=1),
    "temperature": st.slider("temperature", min_value=0.0, max_value=2.0, value=1.0),
    "max_tokens": st.number_input("max_tokens", min_value=1, value=512),
    "top_p": st.slider("top_p", min_value=0.0, max_value=1.0, value=1.0),
    "presence_penalty": st.slider("presence_penalty", min_value=-2.0, max_value=2.0, value=0.0),
    "frequency_penalty": st.slider("frequency_penalty", min_value=-2.0, max_value=2.0, value=0.0),
    "stream": False,
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
  # Assistant message
  assistant_msg = dict(response.choices[0].message)
  # Display assistant message
  with st.chat_message("assistant"):
    st.write(assistant_msg.get("content"))
  # Append to history
  st.session_state.messages.append(assistant_msg)