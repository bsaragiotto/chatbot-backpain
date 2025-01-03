import streamlit as st
from openai import OpenAI

# Your OpenAI API key (exposed)
OPENAI_API_KEY = "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"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Streamlit app logic
st.title("💬 Chat-Back")
st.write(
    "Welcome to Chat-Back! 👋 I'm your friendly assistant here to help you understand and manage back pain. "
    "Whether you're looking for tips, exercises, or general advice, I'm here to provide guidance and support. "
)

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user message
if prompt := st.chat_input("Ask me anything about back pain"):
    # Store and display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )

        # Extract and display the assistant's response
        assistant_message = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
    except Exception as e:
        st.error(f"An error occurred: {e}")
