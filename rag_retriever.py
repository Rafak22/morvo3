# rag_retriever.py
from chroma_memory import query_memory

def retrieve_context(user_query: str) -> str:
    """
    Search vector memory and build a context string from the top chunks.
    """
    try:
        results = query_memory(user_query, top_k=4)
        if not results:
            return ""

        context_texts = [doc.page_content for doc in results]
        context = "\n---\n".join(context_texts)

        return f"""
هذه بعض المعلومات المتعلقة من أرشيف الشركة:

{context}

يرجى استخدام هذه المعلومات عند الإجابة على السؤال التالي.
"""
    except Exception as e:
        # If RAG fails, return empty context
        print(f"RAG retrieval failed: {e}")
        return ""
