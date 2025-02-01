from supervised.scrape import fetch_recent_papers, professors
import scholarly
from scholarly import ProxyGenerator
import time
from dotenv import load_dotenv
import os
import random
from supabase import create_client, Client
import supervised.cache as cache

if __name__ == "__main__":
    try:
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")

        supabase: Client = create_client(url, key)
    except Exception as e:
        print(f"Failed to connect to supabase: {str(e)}")
        exit()

    print("started")
    for professor_name in professors[11:]:
        t = time.time()
        author = cache.author
        papers = cache.papers
        try:
            author, papers = fetch_recent_papers(professor_name, 5)
        except Exception as e:
            print(f"Failed to fetch papers for {professor_name}: {str(e)}")
            continue

        data = {
            "email": author["scholar_id"],
            "profile": author,
            "avatar_url": author["picture_url"],
            "publications": papers,
        }

        response = supabase.table("professors").insert(data).execute()
        print(
            f"Successfully inserted data for {author['name']} in {time.time() - t} seconds"
        )
