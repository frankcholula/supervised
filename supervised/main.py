import streamlit as st
# Streamlit UI with Sidebar
st.set_page_config(page_title="Supervised", layout="wide")

professors = [
    {
        "name": "Prof. John Doe",
        "area": "Computer Vision",
        "h_index": 45,
        "citations": 12000,
        "citations_2020": 4000,
        "top_papers": ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5"],
        "recent_papers": ["Recent 1", "Recent 2", "Recent 3", "Recent 4", "Recent 5"],
        "image": "prof1.jpg",
    },
    {
        "name": "Prof. Jane Smith",
        "area": "Machine Learning on Data",
        "h_index": 60,
        "citations": 18000,
        "citations_2020": 5000,
        "top_papers": ["Paper A", "Paper B", "Paper C", "Paper D", "Paper E"],
        "recent_papers": ["Recent A", "Recent B", "Recent C", "Recent D", "Recent E"],
        "image": "prof2.jpg",
    },
]


with st.sidebar:
    st.markdown(
        "<style>.sidebar .sidebar-content { background-color: #FFA500; }</style>",
        unsafe_allow_html=True,
    )
    st.title("Search Professors")

    area_of_interest = st.text_input(label="Area of Interest", placeholder= "Computer Vision")
    # Ranking Professors

    # Top by Citations
    st.subheader("📌 Ranking by Citations")
    top_citations = sorted(professors, key=lambda x: x["citations"], reverse=True)
    for prof in top_citations[:3]:
        st.sidebar.markdown(f"- **{prof['name']}**: {prof['citations']} citations")

    # Top by Citations & Recent Activity
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
        st.sidebar.markdown(f"- **{prof['name']}**: h-index {prof['h_index']}")

# Display Professors
st.title("Professors in the Field")
col1, col2 = st.columns(2)

for idx, prof in enumerate(professors):
    if area_of_interest.lower() in prof["area"].lower():
        st.markdown(
            f"""
                <div style="
                    background-color: #FF914D; 
                    padding: 20px; 
                    border-radius:20px; 
                    box-shadow: 3px 3px 15px rgba(0,0,0,0.2); 
                    color:      ;
                    display: flex;
                    flex-direction: row;
                    width: 100%;
                    align-items: center;
                    position: relative;">
                 
                    
                    name: {prof['name']}
                    area: {prof['area']}
                    h_index: {prof['h_index']}
                    citations: {prof['citations']}
                    citations_2020: {prof['citations_2020']}
                    top_papers: {', '.join(prof['top_papers'])}
                    recent_papers: {', '.join(prof['recent_papers'])}
                
                </div>
                """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)  # Adds spacing between cards


