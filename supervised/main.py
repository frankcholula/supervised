import streamlit as st
from streamlit_extras.colored_header import colored_header
from supabase import create_client
from streamlit_agraph import agraph, Node, Edge, Config
import plotly.express as px
import pandas as pd
from supervised.rag import get_similar_documents
import numpy as np
from ast import literal_eval

# Streamlit page configuration
st.set_page_config(page_title="Supervised", layout="wide")

# Streamlit tabs
# TODO: Add tabs later to unclutter some data
tab1, tab2, tab3 = st.tabs(["Recommendations", "Network Graph", "Rankings"])


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
                "summary": prof["summary"],
                "summary_embedding": prof["summary_embedding"],
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

    semantic_search = st.text_input(
        "What research topics are you looking for?",
        placeholder="e.g. I love sketching and machine learning!",
    )

    area_of_interest = st.multiselect(
        label="Filter by Areas of Interest",
        options=list(set([area for prof in professors for area in prof["areas"]])),
        placeholder="Your Areas of Interest",
    )


# Function to display ranking
def display_ranking(
    title, ranking_key, profs=professors, top_n=5, additional_info=None
):
    st.subheader(title)
    sorted_profs = sorted(
        profs,
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

    filtered_professors = (
        [
            {
                "name": x["professor"]["profile"]["name"],
                "areas": [
                    area.lower() for area in x["professor"]["profile"]["interests"]
                ],
                "h_index": x["professor"]["profile"]["h_index"],
                "citations": x["professor"]["profile"]["citations"],
                # "citations_2020": 0,  # This would need to be calculated if needed
                "top_papers": [
                    p["title"]
                    for p in x["professor"]["publications"]["most_cited_papers"]
                ],
                "recent_papers": [
                    p["title"] for p in x["professor"]["publications"]["recent_papers"]
                ],
                "image": x["professor"]["profile"]["picture_url"],
                "summary": x["professor"]["summary"],
                "summary_embedding": x["professor"]["summary_embedding"],
            }
            for x in get_similar_documents(semantic_search, 20)
        ]
        if semantic_search and len(semantic_search) > 0
        else [
            prof
            for prof in professors
            if set(prof["areas"]).intersection(area_of_interest)
        ]
    )

    display_ranking(
        "📌 Ranking by Citations",
        lambda x: x["citations"],
        profs=filtered_professors if filtered_professors != [] else professors,
    )
    display_ranking(
        "🏆 Ranking by H-Index",
        lambda x: x["h_index"],
        profs=filtered_professors if filtered_professors != [] else professors,
    )
# Main content
with tab1:
    colored_header("Recommended to You...", description="")

    # Filter professors based on area of interest

    # Display top N professors
    top_matching_professors = 6

    row1 = st.columns(3)
    row2 = st.columns(3)

    for i in range(6):
        if i < len(filtered_professors):
            prof = filtered_professors[i]
            # Select column from appropriate row
            col = row1[i % 3] if i < 3 else row2[i % 3]
            tile = col.container()
            tile.header(f"**{prof['name']}**")
            tile.image(prof["image"], width=200)
            tile.markdown(f"**Areas of Interest**: {', '.join(prof['areas'])}")
            tile.markdown(f"**h-index**: {prof['h_index']}")
            tile.markdown(f"**Citations**: {prof['citations']}")
            tile.markdown(f"{prof['summary']}")
with tab2:
    nodes = []
    edges = []
    use_professors = filtered_professors if filtered_professors != [] else professors
    for prof in use_professors:
        nodes.append(
            Node(
                id=prof["name"],  # using name as unique ID
                size=25,
                shape="circularImage",
                image=prof["image"],
                title=f"Name: {prof['name']}\nAreas: {', '.join(prof['areas'])}\nCitations: {prof['citations']}",
            )
        )

    # Create edges based on similar research areas
    for i, prof1 in enumerate(use_professors):
        for prof2 in use_professors[i + 1 :]:
            # Calculate distance between professor embeddings

            distance = np.linalg.norm(
                np.array(literal_eval(prof1["summary_embedding"]), dtype=float)
                - np.array(literal_eval(prof2["summary_embedding"]), dtype=float)
            )
            threshold = 1.15  # Adjust this threshold as needed

            if distance < threshold:
                # Weight is inverse of distance (closer = stronger connection)
                weight = 1.0 / (
                    distance + 0.0001
                )  # Add small constant to avoid division by zero
                edges.append(
                    Edge(
                        source=prof1["name"],
                        target=prof2["name"],
                        width=weight,  # Edge thickness based on weight
                        title=f"Similarity: {weight:.2f}",  # Show weight on hover,
                        semanticStrokeWidth=True,
                        strokeWidth=500,
                    )
                )

    config = Config(
        width="100%",
        height=1000,
        directed=False,
        physics=True,
        hierarchical=False,
        interaction={"hover": True},
        staticGraphWithDragAndDrop=True,
        semanticStrokeWidth=True,
        strokeWidth=500,
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config,)


with tab3:
    use_professors = filtered_professors if filtered_professors != [] else professors
    if use_professors == []:
        st.warning("No professors found matching your criteria.")
    else:
        df = pd.DataFrame(use_professors)

        def create_scatter_plot():
            st.subheader("H-Index vs. Total Citations")
            fig = px.scatter(
                df,
                x="h_index",
                y="citations",
                size="h_index",
                hover_data=["name", "areas"],
                labels={
                    "h_index": "H-Index",
                    "citations": "Total Citations",
                    "name": "Professor",
                },
            )

            fig.update_layout(
                showlegend=False,
                plot_bgcolor="white",
                width=800,
                height=600,
                hovermode="closest",
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
            st.plotly_chart(fig, use_container_width=True)

        def show_rankings():
            metrics = {"H-Index": "h_index", "Citations": "citations"}

            for title, metric in metrics.items():
                st.subheader(f"Ranking by {title}")
                # Sort dataframe by the current metric in descending order
                sorted_df = df.sort_values(by=metric, ascending=False)
                chart_type = st.scatter_chart if metric == "h_index" else st.bar_chart
                chart_type(data=sorted_df, x="name", y=metric, use_container_width=True)

        create_scatter_plot()
        show_rankings()
