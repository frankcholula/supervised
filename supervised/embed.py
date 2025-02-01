import os
from supabase import create_client, Client
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chonkie import TokenChunker
from tqdm import tqdm
from tokenizers import Tokenizer 

# Initialize Supabase client
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Initialize sentence transformer model and text chunker
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
tokenizer = Tokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")

# Initialize the chunker
chunker = TokenChunker(tokenizer)

def process_professor_papers():
    try:
        # Fetch all professors
        response = supabase.table("professors").select("*").execute()
        professors = response.data

        for professor in tqdm(professors, desc="Processing professors"):
            professor_id = professor["id"]
            
            # Process all papers (both recent and most cited)
            all_papers = (professor["publications"]["recent_papers"] + 
                        professor["publications"]["most_cited_papers"])
            
            for paper in tqdm(all_papers, desc="Processing papers", leave=False):
                abstract = paper["abstract"]
                # Split abstract into chunks using chonky
                chunks = chunker(abstract)
                
                for chunk in tqdm(chunks, desc="Processing chunks", leave=False):
                    # Generate embedding
                    embedding = model.encode(chunk.text)
                    
                    # Insert into documents table
                    doc_data = {
                        "professor_id": professor_id,
                        "text": chunk.text,
                        "embedding": embedding.tolist()  # Convert numpy array to list
                    }
                    
                    supabase.table("documents").insert(doc_data).execute()
        print("Successfully processed all papers and created embeddings")

    except Exception as e:
        print(f"Error processing papers: {str(e)}")

if __name__ == "__main__":
    process_professor_papers()



