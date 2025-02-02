import streamlit as st
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

# Initialize Supabase client
url: str = st.secrets["supabase"]["SUPABASE_URL"]
key: str = st.secrets["supabase"]["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Initialize sentence transformer model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def get_similar_documents(query: str, limit: int = 10):
    """
    Get most similar documents to the query from the documents table.

    Args:
        query (str): The search query
        limit (int): Number of results to return (default 5)

    Returns:
        List of tuples containing (document text, professor data, similarity score)
    """
    try:
        # Generate embedding for the query
        query_embedding = model.encode(query)

        # Convert to list for Supabase
        query_embedding_list = query_embedding.tolist()

        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding_list,
                "match_count": limit,
            },
        ).execute()

        results = []
        # Group documents by professor
        prof_docs = {}
        for doc in response.data:
            # Get professor details for this document
            doc_response = (
                supabase.table("documents")
                .select("professor_id")
                .eq("id", doc["id"])
                .execute()
            )
            if doc_response.data:
                prof_id = doc_response.data[0]["professor_id"]
                prof_response = (
                    supabase.table("professors").select("*").eq("id", prof_id).execute()
                )
                professor = prof_response.data[0] if prof_response.data else None
                
                if professor:
                    if prof_id not in prof_docs:
                        prof_docs[prof_id] = {
                            "professor": professor,
                            "documents": []
                        }
                    prof_docs[prof_id]["documents"].append({
                        "text": doc["text"],
                        "similarity": doc["similarity"]
                    })

        # Sort professors by number of matching documents and flatten results
        for prof_id, data in sorted(
            prof_docs.items(),
            key=lambda x: len(x[1]["documents"]),
            reverse=True
        ):
            # for doc in data["documents"]:
            results.append({
                # "text": data["documents"][0]["text"],
                "professor": data["professor"],
                "number_matches": len(data["documents"]),
                # "similarity": data["documents"][0]["similarity"]
            })

        return results

    except Exception as e:
        print(f"Error getting similar documents: {str(e)}")
        return []


if __name__ == "__main__":
    # Test the RAG function
    query = "I want to apply machine learning to drawing."
    results = get_similar_documents(query)
    print(query)
    print("-" * 50)
    for result in results:
        print(result["professor"]["profile"]["name"], result["number_matches"])
        print(result["professor"]["summary"])
        print("-" * 50)
