import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chat-Back")
st.write(
    "Welcome to Chat-Back! 👋 I'm your friendly assistant here to help you understand and manage back pain. Whether you're looking for tips, exercises, or general advice, I'm here to provide guidance and support."
    "Ask me anything about back pain"
)

# .streamlit/secrets.toml
OPENAI_API_KEY = "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"    

    # Create an OpenAI client.
    client = OpenAI(api_key=["OPENAI_API_KEY"])

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
