import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm

from tools import tools, handle_function_call

def stream_display(response, placeholder):
  text=''
  for chunk in response:
    if parts:=chunk.parts:
      if parts_text:=parts[0].text:
        text += parts_text
        placeholder.write(text + "▌")
  return text

def init_messages() -> None:
  st.session_state.messages = []

def undo() -> None:
  st.session_state.messages.pop()

def set_generate(state=True):
  st.session_state.generate = state


st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by Google Gemini-Pro")

# Google API key
if "api_key" not in st.session_state:
  try:
    st.session_state.api_key = st.secrets["GOOGLE_API_KEY"]
  except:
    st.session_state.api_key = ""
    st.write("Your Google API Key is not provided in `.streamlit/secrets.toml`, but you can input one in the sidebar for temporary use.")

# Initialize chat history
if "messages" not in st.session_state:
  init_messages()
  set_generate(False)

safety_settings={
  'harassment':'block_none',
  'hate':'block_none',
  'sex':'block_none',
  'danger':'block_none'
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
  model_name = st.selectbox("model_name", ['gemini-pro'])
  
  generation_config = {
    "temperature": st.slider("temperature", min_value=0.0, max_value=1.0, value=0.2),
    "max_output_tokens": st.number_input("max_tokens", min_value=1, value=2048),
    "top_k": st.slider("top_k", min_value=1, value=40),
    "top_p": st.slider("top_p", min_value=0.0, max_value=1.0, value=0.95),
  }

  # Tools
  st.header("Tools")
  name_tools = list(tools.keys())
  tools_checkbox = [st.checkbox(n) for n in name_tools]

# Display messages in history
for content in st.session_state.messages:
  if text := content.parts[0].text:
    with st.chat_message('human' if content.role == 'user' else 'ai'):
      st.write(text)

# Chat input
if prompt := st.chat_input("What is up?"):
  if chat_role == 'user':
    set_generate(True)
  # Append to history
  st.session_state.messages.append(
    glm.Content(role=chat_role, parts=[glm.Part(text=prompt)])
  )
  # Display input message
  with st.chat_message('human' if chat_role == 'user' else 'ai'):
    st.write(prompt)

if st.session_state.generate:
  set_generate(False)
  # Generate
  model = genai.GenerativeModel(
    model_name=model_name,
    generation_config=generation_config,
    tools=[tools[name_tools[i]] for i, check in enumerate(tools_checkbox) if check],
  )
  response = model.generate_content(st.session_state.messages, stream=True)
  # Stream display
  with st.chat_message("ai"):
    placeholder = st.empty()
  text = stream_display(response, placeholder)
  # Append to history
  st.session_state.messages.append(response.candidates[0].content)

  # Function calling
  if not text:
    if (content := handle_function_call(response.parts)) is not None:
      text = "Wait for function calling response..."
      placeholder.write(text + "▌")
      st.session_state.messages.append(content)
      response = model.generate_content(st.session_state.messages, stream=True)
      text = stream_display(response, placeholder)
      st.session_state.messages.append(response.candidates[0].content)

  placeholder.write(text)