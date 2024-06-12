import streamlit as st

st.title("Echo Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
if prompt := st.chat_input("What is up?"):
# Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        })
    response = f"(ECHO) {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({
    "role": "assistant",
    "content": response,
    })