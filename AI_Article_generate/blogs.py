import streamlit as st

st.set_page_config(page_title="Blogs")

st.title("Blogs")


def blog_items(title, content):
    with st.expander(title):
        st.markdown(content)


for blog in st.session_state.get("blogs", []):
    print(blog)
    blog_items(blog.title, blog.content)
