import streamlit as st
from pubmed import PubMedRetriever
from chroma_store import ChromaStore
from qa_system import QASystem

# ---------------------
# Streamlit App Layout
# ---------------------
st.set_page_config(page_title="MediAssist AI", layout="wide")
st.title("🩺 MediAssist AI – Healthcare Q&A Tool")
st.markdown("Your AI-powered assistant for **Intermittent Fasting research**.")

# Initialize vector store + QA system
store = ChromaStore()
qa = QASystem()

# ---------------------
# Sidebar: PubMed Search
# ---------------------
st.sidebar.header("🔎 PubMed Search")
search_term = st.sidebar.text_input("Enter search term:", "intermittent fasting obesity diabetes")

if st.sidebar.button("Fetch & Ingest Articles"):
    with st.spinner("Fetching articles from PubMed..."):
        pmids = PubMedRetriever.search_pubmed_articles(search_term, max_results=20)
        articles = PubMedRetriever.fetch_pubmed_abstracts(pmids)
        store.add(articles)
    st.sidebar.success(f"Ingested {len(articles)} articles into vector store ✅")

# ---------------------
# Main Area: Query Bar
# ---------------------
st.subheader("💡 Ask a Question")
user_query = st.text_input("Type your medical question here:")

if st.button("Get Answer"):
    if not user_query.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("Retrieving context and generating answer..."):
            docs, metas = qa.query_vectorstore(user_query, k=3)

            if not docs:
                st.error("No relevant documents found. Try adding more PubMed articles.")
            else:
                prompt = qa.build_prompt(docs, user_query)
                ans = qa.generate_answer(prompt)

                # Display AI Answer
                st.markdown("### 🧾 AI Answer")
                st.write(ans)

                # Expandable Sources
                with st.expander("📚 Sources"):
                    for meta in metas:
                        st.markdown(
                            f"- **{meta['title']}** ({meta['publication_date']}) – *{meta['journal']}*  "
                            f"by {meta['authors']} [PMID: {meta['pmid']}]"
                        )
