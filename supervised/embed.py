import streamlit as st
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from supervised.data import summaries
from chonkie import TokenChunker
from tokenizers import Tokenizer
from transformers import AutoTokenizer


# Initialize Supabase client
url: str = st.secrets["supabase"]["SUPABASE_URL"]
key: str = st.secrets["supabase"]["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Initialize sentence transformer model and text chunker
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
# tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-v3-base")

# Initialize the chunker
# chunker = TokenChunker(tokenizer)


def process_professor_papers():
    try:
        # Fetch all professors
        # response = supabase.table("professors").select("*").execute()
        professors = summaries.keys()

        for professor_id in tqdm(professors, desc="Processing professors"):

            for paper in tqdm(summaries[professor_id], desc="Processing papers", leave=False):                
                # chunks = chunker(paper)
                # chunks = [paper]
                # for chunk in tqdm(chunks, desc="Processing chunks", leave=False):
                    # Generate embedding
                embedding = model.encode(paper)

                # Insert into documents table
                doc_data = {
                    "professor_id": professor_id,
                    "text": paper,
                    "embedding": embedding.tolist(),  # Convert numpy array to list
                }

                supabase.table("documents").insert(doc_data).execute()
        print("Successfully processed all papers and created embeddings")

    except Exception as e:
        print(f"Error processing papers: {str(e)}")


if __name__ == "__main__":
    process_professor_papers()
