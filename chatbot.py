import streamlit as st

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display messages in history
for msg in st.session_state.messages:
  if content := msg.get("content", ""):
    with st.chat_message(msg.get("role")):
      st.write(content)

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

  # Assistant message
  assistant_msg = {
    "role": "assistant",
    "content": f"Echo: {prompt}"
  }
  # Display assistant message
  with st.chat_message("assistant"):
    st.write(assistant_msg.get("content"))
  # Append to history
  st.session_state.messages.append(assistant_msg)