import streamlit as st
from src.logs import fetch_call_logs

st.title("Call Logs")
st.write("This page will display the logs of last 50 calls made using the AutoDialer agent.")

# Refresh controls
if st.button("Refresh", type="primary"):
    # Attempt to clear any cached data (if used) before re-running
    try:
        st.cache_data.clear()
    except Exception:
        pass
    st.rerun()

with st.spinner("Fetching call logs..."):
    call_logs = fetch_call_logs()
    st.table(call_logs)
