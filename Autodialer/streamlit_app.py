import streamlit as st

home_page = st.Page("Home.py", title="Home")
call_logs_page = st.Page("call_logs.py", title="Call Logs")

pg = st.navigation([home_page, call_logs_page])
pg.run()
