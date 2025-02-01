import streamlit as st
from scholarly import scholarly

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
    "Inga Prokopenko"
]

def fetch_scholar_profile(name):
    try:
        search_query = scholarly.search_author(name)
        scholar = next(search_query)
        profile = {
            "name": scholar.get("name"),
            "affiliation": scholar.get("affiliation"),
            "h_index": scholar.get("hindex"),
            "citations": scholar.get("citedby"),
            "interests": scholar.get("interests"),
        }
        
        return profile

    except StopIteration:
        return {"error": f"No profile found for {name}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("hello world")
    # professor_name = "Mark Plumbley"
    # result = fetch_scholar_profile(professor_name)
    # print(result)
