import os
import chromadb
from groq import Groq
import streamlit as st

class QASystem:
    def __init__(self, path="/tmp/chromadb", name="Intermittent_Fasting"):
        self.client = chromadb.PersistentClient(path=path)
        self.col = self.client.get_collection(name=name)
        self.llm = Groq(api_key=st.secrets["GROQ_API_KEY"])

    def query_vectorstore(self, user_query, k=5):
        res = self.col.query(query_texts=[user_query], n_results=k)
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        return docs, metas

    def build_prompt(self, context_docs, user_query):
        context = "\n\n".join(context_docs)
        return f"""You are a helpful medical assistant AI. 
Use the context provided to answer the question. 
If the context does not provide enough information, say so.


Context:
{context}

Question: {user_query}

Answer:"""

    def generate_answer(self, prompt):
        chat = self.llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=500
        )
        return chat.choices[0].message.content


if __name__ == "__main__":
    qa = QASystem()
    user_q = "Does intermittent fasting help improve insulin resistance in Type 2 Diabetes patients?"
    docs, metas = qa.query_vectorstore(user_q, k=3)
    prompt = qa.build_prompt(docs, user_q)
    ans = qa.generate_answer(prompt)
    print("=== AI Answer ===")
    print(ans)
