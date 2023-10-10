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

# ChatCompletion parameters
chat_params = {
  "model": "gpt-3.5-turbo-0613",
  "n": 1,
  "temperature": 1.0,
  "max_tokens": 512,
  "top_p": 1.0,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
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