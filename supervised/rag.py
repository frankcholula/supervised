import os
from supabase import create_client, Client
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Supabase client
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Initialize sentence transformer model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def get_similar_documents(query: str, limit: int = 5):
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
            'match_documents',
            {
                'query_embedding': query_embedding_list,
            }
        ).execute()
        
        results = []
        for doc in response.data:
            # Get professor details for this document
            doc_response = supabase.table("documents").select("professor_id").eq("id", doc["id"]).execute()
            if doc_response.data:
                prof_id = doc_response.data[0]["professor_id"]
                prof_response = supabase.table("professors").select("*").eq("id", prof_id).execute()
                professor = prof_response.data[0] if prof_response.data else None
            else:
                professor = None
            
            results.append({
                'text': doc['text'],
                'professor': professor,
                'similarity': doc['similarity']
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
        print(result['professor']['profile']['name'], result['similarity'])
        print(result['text'])
        print("-" * 50)
