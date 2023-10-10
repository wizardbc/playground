import streamlit as st

def append_history(msgs:list[dict], i:int):
  st.session_state.messages.append(msgs[i])