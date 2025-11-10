import streamlit as st
from src.agent import ArticleGeneratorAgent

st.title("AI Programming Article Generator")
st.write("Generate well-structured programming articles using AI.")

if "blogs" not in st.session_state:
    st.session_state.blogs = []

agent = ArticleGeneratorAgent()
user_query = st.text_area("Enter your article specifications:", height=300)
if st.button("Generate Articles", type="primary"):
    if user_query.strip():
        with st.spinner("Generating articles..."):
            articles = agent.generate_articles(user_query)
            if articles.article_generated and articles.articles:
                st.session_state.blogs.extend(articles.articles)
                st.markdown(
                    "Articled Generated Successfully! Navigate to the 'Blogs' page to view them.")
            else:
                st.error(
                    "No articles were generated. Please check your specifications.")
    else:
        st.error("Please enter article specifications.")
