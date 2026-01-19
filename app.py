import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Quest", layout="wide")

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #fefcf4;
    color: #0b3d0b;
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
}

/* ---------- TOP LOGO (Sticky) ---------- */
.logo-container {
    position: sticky;
    top: 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15px 0;
    background-color: #fefcf4;
    z-index: 9999;
    border-bottom: 2px solid #0b3d0b;
}
.logo-container img {
    width: 60px;
    margin-right: 20px;
}
.logo-container h2 {
    color: #0b3d0b;
    font-weight: bold;
    font-size: 32px;
    margin: 0;
}

/* ---------- LOADING SCREEN ---------- */
.loader-container {
    position: fixed;
    top:0; left:0;
    width:100%;
    height:100vh;
    background: linear-gradient(#e8efe8, #fefcf4);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index:10000;
}
.loader-container h1 {
    color: #0b3d0b;
    font-size: 64px;
    text-align: center;
    margin-bottom:50px;
}
.walker {
    width: 40px;
    height: 80px;
    border: 3px solid #0b3d0b;
    border-radius: 20px;
    position: relative;
    animation: walk 1s infinite alternate;
}
.walker::before {
    content: '';
    width: 12px;
    height: 12px;
    background: #0b3d0b;
    border-radius: 50%;
    position: absolute;
    top: -18px;
    left: 11px;
}
@keyframes walk { 0% { transform: translateX(-25px); } 100% { transform: translateX(25px); } }

.cityscape {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    margin-top:50px;
}
.building {
    width: 30px;
    height: 60px;
    background-color: #0b3d0b;
    margin: 0 5px;
}
.tree {
    width: 20px;
    height: 40px;
    background-color: #145214;
    margin: 0 5px;
    border-radius: 4px;
}

.leaf {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #6b8f71;
    opacity: 0.3;
    border-radius:50%;
    animation: fall 6s linear infinite;
}
@keyframes fall { 0% { transform: translateY(-100px); } 100% { transform: translateY(100vh); } }

/* ---------- FILTER BUTTONS ---------- */
.filter-btn {
    background-color: #0b3d0b;
    color: #fefcf4;
    border-radius: 8px;
    padding: 8px 15px;
    border: none;
    font-weight: bold;
    cursor: pointer;
    margin-right:5px;
}
.filter-btn:hover {
    background-color: #145214;
}

/* ---------- BOTTOM NAVIGATION (Sticky) ---------- */
.nav-container {
    position: sticky;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #fefcf4;
    border-top: 2px solid #0b3d0b;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 10px 0;
    z-index: 9999;
}
.nav-container img {
    width: 50px;
    cursor: pointer;
    transition: transform 0.2s;
}
.nav-container img:hover {
    transform: scale(1.2);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATASET
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("houses.csv")
data = load_data()

# ---------------------------
# SESSION STATES
# ---------------------------
if "loaded" not in st.session_state:
    st.session_state.loaded = False
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "filter_type" not in st.session_state:
    st.session_state.filter_type = "All"
if "price_range" not in st.session_state:
    st.session_state.price_range = (data['price'].min(), data['price'].max())

# ---------------------------
# LOADING SCREEN
# ---------------------------
if not st.session_state.loaded:
    st.markdown(f"""
    <div class="loader-container">
        <h1>Rest Quest</h1>
        <div class="walker"></div>
        <div class="cityscape">
            <div class="building"></div>
            <div class="tree"></div>
            <div class="building"></div>
            <div class="tree"></div>
            <div class="building"></div>
        </div>
        <div class="leaf" style="left:10%;"></div>
        <div class="leaf" style="left:35%;"></div>
        <div class="leaf" style="left:60%;"></div>
        <div class="leaf" style="left:80%;"></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# TOP LOGO
# ---------------------------
st.markdown("""
<div class="logo-container">
    <img src="image-removebg-preview.png" alt="Logo">
    <h2>Rest Quest</h2>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# HOME PAGE
# ---------------------------
st.markdown("<br><br><br>", unsafe_allow_html=True)  # space under sticky header
if st.session_state.page == "Home":
    cols = st.columns([1,1,1])
    with cols[0]:
        if st.button("All", key="all_btn"):
            st.session_state.filter_type = "All"
    with cols[1]:
        if st.button("🏠 Rent", key="rent_btn"):
            st.session_state.filter_type = "Rent"
    with cols[2]:
        if st.button("🏷 Sale", key="sale_btn"):
            st.session_state.filter_type = "Sale"

    st.markdown("---")
    st.header("Recommended Houses")

    filtered = data.copy()
    if st.session_state.filter_type != "All":
        filtered = filtered[filtered["type"] == st.session_state.filter_type]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']}")
        st.write(f"💰 ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SEARCH PAGE
# ---------------------------
elif st.session_state.page == "Search":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.header("Search Houses")
    search_query = st.text_input("Search by name or location")
    
    filtered = data.copy()
    if search_query:
        filtered = filtered[
            filtered["name"].str.contains(search_query, case=False) |
            filtered["location"].str.contains(search_query, case=False)
        ]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']} | 💰 ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SETTINGS PAGE
# ---------------------------
elif st.session_state.page == "Settings":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.header("Settings")
    st.subheader("Get Help")
    st.markdown("""
📧 support@restquest.com  
📘 [How to Use Rest Quest](https://example.com)
""")
    st.subheader("Post Listing")
    st.markdown("""
📧 [Send listing via email](mailto:listings@restquest.com)  
[Instructions for posting a listing](https://example.com/posting-instructions)
""")

# ---------------------------
# BOTTOM NAVIGATION
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(" ", key="nav_home"):
        st.session_state.page = "Home"
    st.markdown('<img src="Home.png" alt="Home">', unsafe_allow_html=True)

with col2:
    if st.button(" ", key="nav_search"):
        st.session_state.page = "Search"
    st.markdown('<img src="Search.png" alt="Search">', unsafe_allow_html=True)

with col3:
    if st.button(" ", key="nav_settings"):
        st.session_state.page = "Settings"
    st.markdown('<img src="Settings.png" alt="Settings">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
