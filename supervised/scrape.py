import random
import streamlit as st
from scholarly import scholarly
import copy
import requests
import os
import time

from supabase import create_client, Client
from dotenv import load_dotenv

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


def download_profile_picture(url, name):
    """Downloads profile picture from Google Scholar and saves it with the author's name

    Args:
        url (str): URL of the profile picture
        name (str): Name of the author to use in filename

    Returns:
        str: Path to saved image file, or None if download failed
    """
    if not url:
        return None

    try:
        os.makedirs("images", exist_ok=True)

        clean_name = "".join(
            x for x in name if x.isalnum() or x in (" ", "-", "_")
        ).rstrip()
        image_path = os.path.join("images", f"{clean_name}.jpg")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        max_retries = 1
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                raise

        with open(image_path, "wb") as f:
            f.write(response.content)

        return image_path

    except Exception as e:
        print(f"Failed to download profile picture: {str(e)}")
        return None


if __name__ == "__main__":
    try:
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        email: str = os.environ.get("SUPABASE_EMAIL")
        password: str = os.environ.get("SUPABASE_PASSWORD")
        supabase: Client = create_client(url, key)
    except Exception as e:
        print(f"Failed to load environment variables: {str(e)}")
        raise e

    print("hello world")
    professor_name = random.choice(professors)
    author = {
        "name": "Ying-Hao Eddie Chu",
        "affiliation": "National Tsing Hua University, National Yang Ming Chiao Tung university, Academia Sinica",
        "h_index": 91,
        "citations": 36476,
        "interests": [
            "Transparent Electronics",
            "Oxides",
            "MICAtronics",
            "van der Waals epitaxy",
            "high entropy materials",
        ],
        "picture_url": "https://scholar.google.com/citations?view_op=medium_photo&user=56HLf2sAAAAJ",
    }
    papers = {
        "recent_papers": [
            {
                "title": "Resistive Switching Behaviors of PbHfO3 RRAM at Atomic Scale",
                "year": 2025,
                "citations": 0,
                "abstract": "Ternary metal oxide-based resistive random access memory (RRAM) is becoming increasingly popular in memory systems owing to its excellent characteristics, such as high switching speed and reliable stability. In this study, dielectric layer PbHfO3 (PHO) films were epitaxially deposited on the SrRuO3 (SRO) bottom electrode, and Au was deposited as the top electrode. PHO shows resistive switching properties, with a uniform distribution of low-resistance state (LRS) and high-resistance state (HRS), and a long retention time (over 104 s). The atomic resolution transmission electron microscope (TEM) and scanning transmission electron microscope (STEM) images demonstrate the structural evolution of PHO before and after switching. Electron energy loss spectroscopy (EELS) and X-ray photoelectron spectroscopy (XPS) further confirmed the resistive switching path. The results demonstrate the exploitability of …",
                "pub_url": "https://www.sciencedirect.com/science/article/pii/S0925838825002427",
                "eprint_url": None,
            }
        ],
        "most_cited_papers": [
            {
                "title": "Above-bandgap voltages from ferroelectric photovoltaic devices",
                "year": 2010,
                "citations": 1833,
                "abstract": "In conventional solid-state photovoltaics, electron–hole pairs are created by light absorption in a semiconductor and separated by the electric field spaning a micrometre-thick depletion region. The maximum voltage these devices can produce is equal to the semiconductor electronic bandgap. Here, we report the discovery of a fundamentally different mechanism for photovoltaic charge separation, which operates over a distance of 1–2 nm and produces voltages that are significantly higher than the bandgap. The separation happens at previously unobserved nanoscale steps of the electrostatic potential that naturally occur at ferroelectric domain walls in the complex oxide BiFeO3. Electric-field control over domain structure allows the photovoltaic effect to be reversed in polarity or turned off. This new degree of control, and the high voltages produced, may find application in optoelectronic devices.",
                "pub_url": "https://www.nature.com/articles/nnano.2009.451",
                "eprint_url": None,
            }
        ],
    }

    try:
        data = {
            "email": f"{author['name'].lower().replace(' ', '.')}@surrey.ac.uk",
            "profile": author,
            "avatar_url": author["picture_url"],
            "publications": papers,
        }

        response = supabase.table("professors").insert(data).execute()
        print(f"Successfully inserted data for {author['name']}")

    except Exception as e:
        print(f"Failed to insert data into Supabase: {str(e)}")

    # author, papers = fetch_recent_papers(professor_name, 1)

    # for paper in papers['recent_papers']:
    #     print(paper)
    # for paper in papers['most_cited_papers']:
    #     print(paper)
    # author = {'name': 'Joaquin M. Prada Jiménez de Cisneros', 'affiliation': 'Senior Lecturer - University of Surrey', 'h_index': 21, 'citations': 1195, 'interests': ['Mathematical Modelling', 'Immune System', 'Networks', 'Epidemiology'], 'picture_url': 'https://scholar.google.com/citations?view_op=medium_photo&user=29wOkzEAAAAJ'}
    # picture_path = download_profile_picture(author["picture_url"], author["name"])
