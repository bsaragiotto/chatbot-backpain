import streamlit as st
from openai import OpenAI

# Debugging: Inspect secrets
st.write("Loaded secrets:", st.secrets)

# Check for the API key
if "OPENAI_API_KEY" not in st.secrets:
    st.error("API key not found. Please check your secrets configuration.")
    st.stop()

# Set OpenAI API key from secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

# Streamlit app logic
st.title("💬 Chat-Back")
st.write("Welcome to Chat-Back! Ask me anything about back pain.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        st.session_state.messages.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
        with st.chat_message("assistant"):
            st.markdown(response["choices"][0]["message"]["content"])
    except Exception as e:
        st.error(f"An error occurred: {e}")
