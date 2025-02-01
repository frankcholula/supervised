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
        # Search for the author
        search_query = scholarly.search_author(name)
        author = next(search_query)
        
        # Fill in author details including publications
        author = scholarly.fill(author, sections=['publications'])
        
        # Get publications and sort by year for recent papers
        publications = author['publications']
        sorted_by_year = sorted(publications, key=lambda x: x['bib'].get('pub_year', '0'), reverse=True)
        
        # Sort by citations for most cited papers
        sorted_by_citations = sorted(publications, key=lambda x: x.get('num_citations', 0), reverse=True)
        
        # Get the papers
        recent_papers = []
        cited_papers = []
        
        # Process recent papers
        for pub in sorted_by_year[:num_papers]:
            filled_pub = scholarly.fill(pub, sections=['bib', 'num_citations'])
            paper = {
                'title': filled_pub['bib'].get('title'),
                'year': filled_pub['bib'].get('pub_year'),
                'venue': filled_pub['bib'].get('venue'),
                'citations': filled_pub.get('num_citations', 0),
                'abstract': filled_pub['bib'].get('abstract', 'Abstract not available')
            }
            recent_papers.append(paper)
            
        # Process most cited papers
        for pub in sorted_by_citations[:num_papers]:
            # Skip if paper is already in recent papers to avoid duplicate API calls
            if pub['bib'].get('title') in [p['title'] for p in recent_papers]:
                continue
                
            filled_pub = scholarly.fill(pub, sections=['bib', 'num_citations'])
            paper = {
                'title': filled_pub['bib'].get('title'),
                'year': filled_pub['bib'].get('pub_year'),
                'venue': filled_pub['bib'].get('venue'),
                'citations': filled_pub.get('num_citations', 0),
                'abstract': filled_pub['bib'].get('abstract', 'Abstract not available')
            }
            cited_papers.append(paper)
            
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
    professor_name = "Mark Plumbley"
    papers = fetch_recent_papers(professor_name, 3)
    print(papers)
    # result = fetch_scholar_profile(professor_name)
    # print(result)
