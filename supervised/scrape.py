import random
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

def fetch_recent_papers(name, num_papers=5):
    try:
        search_query = scholarly.search_author(name)
        author = next(search_query)
        
        author = scholarly.fill(author, sections=['publications'], sortby='year')
                
        publications = author['publications']
        
        sorted_by_year = sorted(publications, key=lambda x: x['bib'].get('pub_year', '0'), reverse=True)
        sorted_by_citations = sorted(publications, key=lambda x: x.get('num_citations', 0), reverse=True)
    
        recent_papers = []
        cited_papers = []
        
        used_titles = set()

        def add_papers(source_pubs, target_array, num_papers):        
            def process_paper(pub):
                filled_pub = scholarly.fill(pub, sections=['bib', 'num_citations'])
                return {
                    'title': filled_pub['bib'].get('title'),
                    'year': filled_pub['bib'].get('pub_year'),
                    'citations': filled_pub.get('num_citations', 0),
                    'abstract': filled_pub['bib'].get('abstract', 'Abstract not available')
                }
            
            for pub in source_pubs[:num_papers]:
                if pub['bib'].get('title') in used_titles:
                    continue
                paper = process_paper(pub)
                target_array.append(paper)
                used_titles.add(paper['title'])
                
        add_papers(sorted_by_year, recent_papers, num_papers)
        add_papers(sorted_by_citations, cited_papers, num_papers)
            
        return {
            'recent_papers': recent_papers,
            'most_cited_papers': cited_papers
        }

    except StopIteration:
        return {"error": f"No profile found for {name}"}
    except Exception as e:
        return {"error": str(e)}
    
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
    professor_name = random.choice(professors)
    papers = fetch_recent_papers(professor_name, 2)
    print(papers)
    # result = fetch_scholar_profile(professor_name)
    # print(result)
