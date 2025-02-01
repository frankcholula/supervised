import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)



# get table schema
try:
    response = supabase.table("professors").select("*").execute()
    print(response)
except Exception as e:
    print(f"Error: {e}")