import random
import streamlit as st
from scholarly import scholarly
import copy
import supervised.cache as cache

from supabase import create_client, Client

professors = [
    "Mark Plumbley",
    "Yi-Zhe Song",
    "Eddy Zhu",
    "Wenwu Wang",
    "Miroslaw Bober",
    "Phillip Jackson",
    "Muhammad Rana",
    "Kevin Wells",
    "Simon Hadfield",
    "Samaneh Kouchaki",
    "Jean-Yves Guillemaut",
    "Lucia Florescu",
    "Anjan Dutta",
    "Yulia Gryaditskaya",
    "Marco Volino",
    "Gustavo Carneiro",
    "Armin Mustafa",
    "Sameed Husain",
    "Erick Seprandio",
    "Jaoquin Prada",
    "Tony Onoja",
    "Matt Spick",
    "Ullrich Bartsch",
    "Inga Prokopenko",
]


def fetch_recent_papers(name, num_papers=5):
    try:
        search_query = scholarly.search_author(name)
        author = next(search_query)

        # Get publications sorted by year
        author_by_year = scholarly.fill(
            copy.deepcopy(author),
            sections=["basics", "indices", "num_citations", "publications"],
            publication_limit=num_papers,
            sortby="year",
        )
        # Get publications sorted by citations
        author_by_citations = scholarly.fill(
            copy.deepcopy(author),
            sections=["publications"],
            publication_limit=num_papers,
            sortby="citedby",
        )

        profile = {
            "scholar_id": author_by_year.get("scholar_id"),
            "name": author_by_year.get("name"),
            "affiliation": author_by_year.get("affiliation"),
            "h_index": author_by_year.get("hindex"),
            "citations": author_by_year.get("citedby"),
            "interests": author_by_year.get("interests"),
            "picture_url": author_by_year.get("url_picture"),
        }

        recent_papers = []
        cited_papers = []

        def process_papers(publications, target_array):
            for pub in publications:
                filled_pub = scholarly.fill(
                    pub, sections=["bib", "pub_url", "eprint_url", "num_citations"]
                )
                paper = {
                    "title": filled_pub["bib"].get("title"),
                    "year": filled_pub["bib"].get("pub_year"),
                    "citations": filled_pub.get("num_citations", 0),
                    "abstract": filled_pub["bib"].get(
                        "abstract", "Abstract not available"
                    ),
                    "pub_url": filled_pub.get("pub_url"),
                    "eprint_url": filled_pub.get("eprint_url"),
                }
                target_array.append(paper)

        process_papers(author_by_year["publications"], recent_papers)
        process_papers(author_by_citations["publications"], cited_papers)

        return profile, {
            "recent_papers": recent_papers,
            "most_cited_papers": cited_papers,
        }

    except StopIteration:
        return {"error": f"No profile found for {name}"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    try:
        url: str = st.secrets["supabase"]["SUPABASE_URL"]
        key: str = st.secrets["supabase"]["SUPABASE_KEY"]

        supabase: Client = create_client(url, key)

        print("hello world")
        professor_name = random.choice(professors)

        author = cache.author
        papers = cache.papers
        # author, papers = fetch_recent_papers(professor_name, 5)
        author, papers = cache.author, cache.papers

        data = {
            "email": author["scholar_id"],
            "profile": author,
            "avatar_url": author["picture_url"],
            "publications": papers,
        }

        response = supabase.table("professors").insert(data).execute()
        print(f"Successfully inserted data for {author['name']}")

    except Exception as e:
        print(f"Failed: {str(e)}")
