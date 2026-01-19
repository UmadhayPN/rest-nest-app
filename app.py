import streamlit as st
import pandas as pd
import time
from PIL import Image

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
    background-color: #f7f7f2;
    color: #0b3d0b;
    font-family: sans-serif;
}

/* ---------- TOP LOGO ---------- */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px 0 20px 0;
}
.logo-container img {
    width: 50px;
    margin-right: 15px;
}

/* ---------- LOADING SCREEN ---------- */
.loader-container {
    height: 100vh;
    background: linear-gradient(#e8efe8, #f7f7f2);
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

@keyframes walk {
    0% { transform: translateX(-25px); }
    100% { transform: translateX(25px); }
}

.leaf {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #6b8f71;
    opacity: 0.3;
    animation: fall 6s linear infinite;
}

@keyframes fall {
    0% { transform: translateY(-100px); }
    100% { transform: translateY(100vh); }
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

/* Bottom nav buttons as images */
.nav-container img {
    width: 40px;
    cursor: pointer;
}

.nav-container img:hover {
    transform: scale(1.1);
    transition: 0.2s;
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
        <div class="walker"></div>
        <h1>Rest Quest</h1>
        <p>Finding your next home...</p>
        <div class="leaf" style="left:15%"></div>
        <div class="leaf" style="left:45%"></div>
        <div class="leaf" style="left:75%"></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# TOP LOGO (Image + Text)
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
if st.session_state.page == "Home":
    f1, f2 = st.columns(2)
    with f1:
        if st.button("🏠 Rent"):
            st.session_state.filter_type = "Rent"
    with f2:
        if st.button("🏷 Sale"):
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
        st.write(f"{row['location']} | ₱{row['price']:,}")
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

**Instructions for posting a listing:**  
[Click here to view detailed posting instructions](https://example.com/posting-instructions)
""")

# ---------------------------
# SPACE FOR NAV BAR
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAVIGATION (Image Logos)
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.image("Home.png", use_column_width=False, output_format="PNG"):
        st.session_state.page = "Home"

with col2:
    if st.image("Search.png", use_column_width=False, output_format="PNG"):
        st.session_state.page = "Search"

with col3:
    if st.image("Settiing.png", use_column_width=False, output_format="PNG"):
        st.session_state.page = "Settings"

st.markdown('</div>', unsafe_allow_html=True)

