import streamlit as st
from .openai import Stream2Msgs

def append_history(msgs:Stream2Msgs, i:int):
  msg = msgs.msgs[i]
  if content := msg.get("content", ""):
    st.session_state.messages.append({
      "role": "assistant",
      "content": content,
    })
  if f_name := msg.get("function_call", {}).get("name", ""):
    st.session_state.messages.append({
      "role": "assistant",
      "content": "",
      "function_call": {
        "name": f_name,
        "arguments": msg.get("function_call").get("arguments")
      }
    })

def undo():
  st.session_state.messages = st.session_state.messages[:-1]