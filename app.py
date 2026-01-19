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

/* ---------- TOP LOGO ---------- */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
}
.logo-container img {
    width: 50px;
    margin-right: 15px;
}
.logo-container h2 {
    color: #0b3d0b;
    font-weight: bold;
    font-size: 36px;
    margin: 0;
}

/* ---------- LOADING SCREEN ---------- */
.loader-container {
    height: 100vh;
    background: linear-gradient(#e8efe8, #fefcf4);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
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

/* ---------- CITY BUILDINGS AND TREES ---------- */
.cityscape {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    width: 100%;
    height: 100px;
    margin-top: 20px;
}
.building {
    width: 40px;
    height: 80px;
    background: #0b3d0b;
    margin: 0 5px;
    border-radius: 2px;
}
.tree {
    width: 25px;
    height: 50px;
    background: #145214;
    margin: 0 5px;
    border-radius: 5px;
}

/* ---------- FALLING LEAVES ---------- */
.leaf {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #6b8f71;
    opacity: 0.3;
    border-radius: 50%;
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
}
.filter-btn:hover {
    background-color: #145214;
}

/* ---------- FIXED BOTTOM NAV ---------- */
.nav-container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #ffffff;
    border-top: 2px solid #0b3d0b;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 5px 0;
    z-index: 9999;
}
.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-weight: bold;
    color: #0b3d0b;
    cursor: pointer;
}
.nav-item img {
    width: 40px;
    margin-bottom: 5px;
    transition: transform 0.2s;
}
.nav-item:hover img {
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

# ---------------------------
# LOADING SCREEN
# ---------------------------
if not st.session_state.loaded:
    st.markdown("""
    <div class="loader-container">
        <h1 style="color:#0b3d0b; font-size:48px;">Rest Quest</h1>
        <div class="walker"></div>
        <div class="cityscape">
            <div class="building"></div>
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
    <img src="logo.png" alt="Logo">
    <h2>Rest Quest</h2>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# HOME PAGE
# ---------------------------
if st.session_state.page == "Home":
    col_all, col_rent, col_sale = st.columns(3)
    with col_all:
        if st.button("All", key="all_btn"):
            st.session_state.filter_type = "All"
    with col_rent:
        if st.button("🏠 Rent", key="rent_btn"):
            st.session_state.filter_type = "Rent"
    with col_sale:
        if st.button("🏷 Sale", key="sale_btn"):
            st.session_state.filter_type = "Sale"

    st.markdown("---")
    st.header("Recommended Houses")

    filtered = data.copy()
    if st.session_state.filter_type != "All":
        filtered = filtered[filtered["type"] == st.session_state.filter_type]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']} | 💰 ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SEARCH PAGE
# ---------------------------
elif st.session_state.page == "Search":
    st.header("Search Houses")
    search_query = st.text_input("Search by name or location")
    location_filter = st.selectbox("Filter by Location", ["All"] + list(data["location"].unique()))
    price_filter = st.slider("Price Range", int(data["price"].min()), int(data["price"].max()), (int(data["price"].min()), int(data["price"].max())))

    filtered = data.copy()
    if search_query:
        filtered = filtered[
            filtered["name"].str.contains(search_query, case=False) |
            filtered["location"].str.contains(search_query, case=False)
        ]
    if location_filter != "All":
        filtered = filtered[filtered["location"] == location_filter]
    filtered = filtered[(filtered["price"] >= price_filter[0]) & (filtered["price"] <= price_filter[1])]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']} | 💰 ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SETTINGS PAGE
# ---------------------------
elif st.session_state.page == "Settings":
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
# SPACE FOR NAV BAR
# ---------------------------
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAVIGATION
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("Home", key="nav_home"): st.session_state.page="Home"
    st.markdown('<div class="nav-item"><img src="home.png"><span>Home</span></div>', unsafe_allow_html=True)

with nav_col2:
    if st.button("Search", key="nav_search"): st.session_state.page="Search"
    st.markdown('<div class="nav-item"><img src="search.png"><span>Search</span></div>', unsafe_allow_html=True)

with nav_col3:
    if st.button("Settings", key="nav_settings"): st.session_state.page="Settings"
    st.markdown('<div class="nav-item"><img src="settings.png"><span>Settings</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
