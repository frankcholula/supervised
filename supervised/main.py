import streamlit as st
from streamlit_extras.colored_header import colored_header

# Data for professors
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

# Streamlit page configuration
st.set_page_config(page_title="Supervised", layout="wide")

# Sidebar configuration
with st.sidebar:
    st.markdown(
        "<style>.sidebar .sidebar-content { background-color: #FFA500; }</style>",
        unsafe_allow_html=True,
    )
    st.subheader("🔍 Search Your Professor")

    area_of_interest = st.multiselect(
        label="Areas of Interest",
        options=["Computer Vision", "Machine Learning on Data"],
        placeholder="Your Areas of Interest",
    )

# Function to display ranking
def display_ranking(title, ranking_key, top_n=3, additional_info=None):
    st.subheader(title)
    sorted_profs = sorted(professors, key=ranking_key, reverse=True)
    for prof in sorted_profs[:top_n]:
        info = f"- **{prof['name']}**: {ranking_key(prof)}"
        if additional_info:
            info += f", {additional_info(prof)}"
        st.markdown(info)

# Display rankings in the sidebar
with st.sidebar:
    display_ranking("📌 Ranking by Citations", lambda x: x["citations"])
    display_ranking(
        "🏃 Ranking by Recent Activity",
        lambda x: x["citations"] + x["citations_2020"],
        additional_info=lambda x: f"{x['citations']} total, {x['citations_2020']} since 2020",
    )
    display_ranking("🏆 Ranking by H-Index", lambda x: x["h_index"])

# Main content
colored_header("Recommended to You...", description="")

# Filter professors based on area of interest
filtered_professors = [prof for prof in professors if prof["area"] in area_of_interest]

# Display top 3 professors
row = st.columns(3)
for i, col in enumerate(row):
    if i < len(filtered_professors):
        prof = filtered_professors[i]
        tile = col.container()
        tile.header(f"**{prof['name']}**")
        tile.image(prof["image"], use_container_width=True)
        tile.markdown(f"Area: {prof['area']}")
        tile.markdown(f"h-index: {prof['h_index']}")
        tile.markdown(f"Citations: {prof['citations']}")
        tile.markdown(f"Citations 2020: {prof['citations_2020']}")
