import streamlit as st

home_page = st.Page("main.py", title="Home")
blogs_page = st.Page("blogs.py", title="Blogs")

pg = st.navigation([home_page, blogs_page])
pg.run()
