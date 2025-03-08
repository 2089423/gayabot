import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title(" Gaya3's Health & Well-being Chatbot 🏥💊")

# Display a disclaimer
st.markdown(
    "⚠️ **Disclaimer:** This chatbot provides general health-related information but is *not a substitute for professional medical consultation*. Always seek advice from a qualified healthcare provider."
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input
user_input = st.chat_input("Ask me about health, diseases, medicine, or nutrition...")

# Function to get a response from OpenAI with health-related context
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # System instruction to enforce health-related responses only
            {
                "role": "system",
                "content": (
                    "You are a virtual health assistant. You can only discuss topics related to health, diseases, symptoms, medicine, home remedies, pharmaceuticals, "
                    "nutrition, exercise, and overall well-being. If the user asks about unrelated topics (such as politics, technology, entertainment, finance), "
                    "politely refuse and encourage them to ask about health-related matters."
                ),
            }
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# List of health-related keywords for filtering
health_keywords = [
    "health", "disease", "symptom", "medicine", "remedy", "nutrition",
    "exercise", "well-being", "pharmaceutical", "treatment", "infection",
    "vaccine", "doctor", "diet", "pain", "fever", "cough", "headache", 
    "cold", "fatigue", "therapy", "injury", "surgery", "immune", "wellness"
]

# Process and display response if there's input
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check if the input is related to health topics (Negative Prompting)
    if not any(keyword in user_input.lower() for keyword in health_keywords):
        assistant_response = (
            "I can only discuss health-related topics such as diseases, symptoms, medicine, home remedies, nutrition, and overall well-being. "
            "Please ask me something related to these topics. 🏥💊"
        )
    else:
        assistant_response = get_response(user_input)

    # Append messages to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
