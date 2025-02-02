import streamlit as st
from streamlit_extras.colored_header import colored_header
from supabase import create_client, Client
from streamlit_agraph import agraph, Node, Edge, Config

# Streamlit page configuration
st.set_page_config(page_title="Supervised", layout="wide")

# Streamlit tabs
# TODO: Add tabs later to unclutter some data
tab1, tab2, tab3 = st.tabs(["Recommendations", "Network Graph", "Visualizations"])


@st.cache_resource
def init_connection():
    url: str = st.secrets["supabase"]["SUPABASE_URL"]
    key: str = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)


@st.cache_data(ttl=600)
def fetch_professors():
    try:
        supabase = init_connection()
        response = supabase.table("professors").select("*").execute()
        professors_data = response.data
        print(len(professors_data))
        professors = []
        for prof in professors_data:
            profile = prof["profile"]
            publications = prof["publications"]
            print(profile)
            professor = {
                "name": profile["name"],
                "areas": [area.lower() for area in profile["interests"]],
                "h_index": profile["h_index"],
                "citations": profile["citations"],
                # "citations_2020": 0,  # This would need to be calculated if needed
                "top_papers": [p["title"] for p in publications["most_cited_papers"]],
                "recent_papers": [p["title"] for p in publications["recent_papers"]],
                "image": profile["picture_url"],
            }
            professors.append(professor)

        return professors
    except Exception as e:
        st.error(f"Error fetching professor data: {str(e)}")
        return []


professors = fetch_professors()

# Sidebar configuration
with st.sidebar:
    st.markdown(
        "<style>.sidebar .sidebar-content { background-color: #FFA500; }</style>",
        unsafe_allow_html=True,
    )
    st.subheader("🔍 Search Your Professor")

    area_of_interest = st.multiselect(
        label="Areas of Interest",
        options=list(set([area for prof in professors for area in prof["areas"]])),
        placeholder="Your Areas of Interest",
    )


# Function to display ranking
def display_ranking(title, ranking_key, top_n=5, additional_info=None):
    st.subheader(title)
    sorted_profs = sorted(
        (
            professors
            if len(area_of_interest) == 0
            else [
                prof
                for prof in professors
                if set(prof["areas"]).intersection(area_of_interest)
            ]
        ),
        key=ranking_key,
        reverse=True,
    )
    for prof in sorted_profs[:top_n]:
        info = f"- **{prof['name']}**: {ranking_key(prof)}"
        if additional_info:
            info += f", {additional_info(prof)}"
        st.markdown(info)


# Display rankings in the sidebar
with st.sidebar:
    display_ranking("📌 Ranking by Citations", lambda x: x["citations"])
    display_ranking("🏆 Ranking by H-Index", lambda x: x["h_index"])


# Main content
with tab1:
    colored_header("Recommended to You...", description="")

    # Filter professors based on area of interest
    filtered_professors = [
        prof for prof in professors if set(prof["areas"]).intersection(area_of_interest)
    ]

    # Display top N professors
    top_matching_professors = 5

    row = st.columns(top_matching_professors)
    for i, col in enumerate(row):
        if i < len(filtered_professors):
            prof = filtered_professors[i]
            tile = col.container()
            tile.header(f"**{prof['name']}**")
            tile.image(prof["image"], use_container_width=True)
            tile.markdown(f"**Areas of Interest**: {', '.join(prof['areas'])}")
            tile.markdown(f"**h-index**: {prof['h_index']}")
            tile.markdown(f"**Citations**: {prof['citations']}")

with tab2:
    nodes = []
    edges = []

    for prof in professors:
        nodes.append(
            Node(
                id=prof["name"],  # using name as unique ID
                size=25,
                shape="circularImage",
                image=prof["image"],
                title=f"Name: s{prof['name']}\nAreas: {', '.join(prof['areas'])}\nCitations: {prof['citations']}",
            )
        )

    # Create edges based on similar research areas
    for i, prof1 in enumerate(professors):
        for prof2 in professors[i + 1 :]:
            # Create edge if professors share any research areas
            common_areas = set(prof1["areas"]) & set(prof2["areas"])
            if common_areas:
                edges.append(
                    Edge(
                        source=prof1["name"],
                        target=prof2["name"],
                    )
                )

    config = Config(
        width="100%",
        height=1000,
        directed=False,
        physics=True,
        hierarchical=False,
        interaction={"hover": True},
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)
