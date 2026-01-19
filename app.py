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
    background-color: #f7f7f2; /* off white */
    color: #0b3d0b; /* dark green */
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
    padding: 10px 0;
    border-top: 2px solid #0b3d0b;
    z-index: 9999;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    background-color: transparent;
    color: #0b3d0b;
    border: none;
    font-size: 16px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #e6f0e6;
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
    <img src="image-removebg-preview.png" alt="crazy">
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
- Include a detailed description  
- Specify price range  
- Indicate if it is for Rent or Sale  
- Provide a clear and searchable title  
- Category and place  
- Size of the house  
- Availability  
- Condition of the house  
- Include photos if possible
""")

# ---------------------------
# SPACE FOR NAV BAR
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# FIXED BOTTOM NAVIGATION (placeholders for logos)
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)

with n1:
    if st.button("🏠 Home", key="nav_home"):
        st.session_state.page = "Home"

with n2:
    if st.button("🔍 Search", key="nav_search"):
        st.session_state.page = "Search"

with n3:
    if st.button("⚙️ Settings", key="nav_settings"):
        st.session_state.page = "Settings"

st.markdown('</div>', unsafe_allow_html=True)

