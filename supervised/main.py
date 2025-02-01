import streamlit as st

professors = [
    {
        "name": "Prof. John Doe",
        "area": "Computer Vision",
        "h_index": 45,
        "citations": 12000,
        "citations_2020": 4000,
        "top_papers": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5"],
        "recent_papers": ["Recent 1", "Recent 2", "Recent 3", "Recent 4", "Recent 5"],
        "image": "supervised/prof1.jpg",
    },
    {
        "name": "Prof. Jane Smith",
        "area": "Machine Learning on Data",
        "h_index": 60,
        "citations": 18000,
        "citations_2020": 5000,
        "top_papers": ["Paper A", "Paper B", "Paper C", "Paper D", "Paper E"],
        "recent_papers": ["Recent A", "Recent B", "Recent C", "Recent D", "Recent E"],
        "image": "supervised/prof2.jpg",
    },
]

st.set_page_config(page_title="Supervised", layout="wide")
with st.sidebar:
    st.markdown(
        "<style>.sidebar .sidebar-content { background-color: #FFA500; }</style>",
        unsafe_allow_html=True,
    )
    st.title("Search Professors")

    area_of_interest = st.text_input(label="Area of Interest", placeholder= "Computer Vision")

    st.subheader("📌 Ranking by Citations")
    top_citations = sorted(professors, key=lambda x: x["citations"], reverse=True)
    for prof in top_citations[:3]:
        st.markdown(f"- **{prof['name']}**: {prof['citations']} citations")

    st.subheader("🔥 Ranking by Recent Activity")
    top_recent = sorted(
        professors, key=lambda x: x["citations"] + x["citations_2020"], reverse=True
    )
    for prof in top_recent[:3]:
        st.markdown(
            f"- **{prof['name']}**: {prof['citations']} total, {prof['citations_2020']} since 2020"
        )
    # Top by H-Index
    st.subheader("🏆 Ranking by H-Index")
    top_h_index = sorted(professors, key=lambda x: x["h_index"], reverse=True)
    for prof in top_h_index[:3]:
        st.markdown(f"- **{prof['name']}**: h-index {prof['h_index']}")


st.title("Professors in the Field")
# Only select top 3 professors
row = st.columns(3)

for col in row:
    tile = col.container(border=True)
    tile.header(f"**{professors[0]['name']}**")

    tile.image(professors[0]["image"], use_container_width=True)
    tile.markdown(f"Area: {professors[0]['area']}")
    tile.markdown(f"h-index: {professors[0]['h_index']}")
    tile.markdown(f"Citations: {professors[0]['citations']}")
    tile.markdown(f"Citations 2020: {professors[0]['citations_2020']}")


