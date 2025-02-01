import streamlit as st
from supabase import create_client, Client


url: str = st.secrets["supabase"]["SUPABASE_URL"]
key: str = st.secrets["supabase"]["SUPABASE_KEY"]
supabase: Client = create_client(url, key)


# get table schema
try:
    response = supabase.table("professors").select("*").execute()
    print(response)
except Exception as e:
    print(f"Error: {e}")
