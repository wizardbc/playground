import streamlit as st
from PIL import Image
import google.generativeai as genai

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by Google Gemini")

# Google API key
if "api_key" not in st.session_state:
  try:
    st.session_state.api_key = st.secrets["GOOGLE_API_KEY"]
  except:
    st.session_state.api_key = ""
    st.write("Your Google API Key is not provided in `.streamlit/secrets.toml`, but you can input one in the sidebar for temporary use.")

def init_messages() -> None:
  st.session_state.messages = []
  st.session_state.img_file_buffer = None

def undo() -> None:
  st.session_state.messages.pop()

def set_generate(state=True):
  st.session_state.generate = state

# Initialize chat history
if "messages" not in st.session_state:
  init_messages()
  set_generate(False)

safety_settings={
  'harassment':'block_none',
  'hate':'block_none',
  'sex':'block_none',
  'danger':'block_none',
}

# Sidebar for parameters
with st.sidebar:
  # Google API Key
  if not st.session_state.api_key:
    st.header("Google API Key")
    st.session_state.api_key = st.text_input("Google API Key", type="password")
  else:
    genai.configure(api_key=st.session_state.api_key)

  # Role selection and Undo
  st.header("Chat")
  chat_role = st.selectbox("role", ["user", "model"], index=0)
  columns = st.columns([1,1,1])
  with columns[0]:
    st.button("Run", on_click=set_generate, type='primary', use_container_width=True)
  with columns[1]:
    st.button("Undo", on_click=undo, use_container_width=True)
  with columns[2]:
    st.button("Clear", on_click=init_messages, use_container_width=True)

  # ChatCompletion parameters
  st.header("Parameters")
  model_name = st.selectbox("model_name",
      ['gemini-pro', 'gemini-pro-vision'])
  generation_config = {
    "temperature": st.slider("temperature", min_value=0.0, max_value=1.0, value=0.9),
    "max_output_tokens": st.number_input("max_tokens", min_value=1, value=2048),
    "top_k": st.slider("top_k", min_value=1, value=1),
    "top_p": st.slider("top_p", min_value=0.0, max_value=1.0, value=1.0),
  }

# Camera input
if model_name == 'gemini-pro-vision':
  if st.session_state.img_file_buffer is None:
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None:
      st.session_state.img_file_buffer = img_file_buffer
    uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'png'])
    if uploaded_file is not None:
      st.session_state.img_file_buffer = uploaded_file
  else:
    st.image(st.session_state.img_file_buffer)
  st.write("* The vision model `gemini-pro-vision` is not optimized for multi-turn chat.")

# Display messages in history
for msg in st.session_state.messages:
  if parts := msg.get("parts", []):
    with st.chat_message('human' if msg.get("role") == 'user' else 'ai'):
      for p in parts:
        st.write(p)

# Chat input
if prompt := st.chat_input("What is up?"):
  # User message
  user_msg = {
    "role": chat_role,
    "parts": [prompt]
  }

  # Display user message
  with st.chat_message('human' if chat_role == 'user' else 'ai'):
    st.write(prompt)
  # Append to history
  st.session_state.messages.append(user_msg)

  if chat_role == 'user':
    set_generate(True)

if st.session_state.generate:
  set_generate(False)
  # Generate
  model = genai.GenerativeModel(model_name=model_name,
                                generation_config=generation_config,
                                safety_settings=safety_settings)
  if model_name == 'gemini-pro-vision':
    if st.session_state.img_file_buffer is not None:
      img = Image.open(st.session_state.img_file_buffer)
      response = model.generate_content([prompt, img], stream=True)
  else:
    response = model.generate_content(st.session_state.messages, stream=True)

  # Stream display
  with st.chat_message("ai"):
    placeholder = st.empty()
  text = ''
  for chunk in response:
    text += chunk.text
    placeholder.write(text + "▌")
  placeholder.write(text)
  # Save the answer
  st.session_state.messages.append({
    'role': 'model',
    'parts': [text]
  })