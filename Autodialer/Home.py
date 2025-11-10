import streamlit as st
from src.agent import AutodialerAgent

st.title("AutoDialer")
st.write("Welcome to the AutoDialer application!")
st.write("Please provide the mobile number with country code and message to initiate a call. (Only verified numbers are allowed due to Twilio trial account limitations.)")

agent = AutodialerAgent()

user_query = st.text_area("Enter your message:", height=150)
if st.button("Make Call", type="primary"):
    if user_query.strip():
        response = None
        with st.spinner("Processing your request..."):
            response = agent.call_agent(user_query.strip())
        st.write("Response from AutoDialer:")
        st.markdown(response["structured_response"].final_response)
    else:
        st.error("Some error occurred. Please try again.")
