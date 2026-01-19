import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Quest", layout="centered")

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #fefcf4;
    color: #0b3d0b;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- CENTER ALL CONTENT ---------- */
.css-18e3th9 {  /* Streamlit main container */
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

/* ---------- TOP LOGO ---------- */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 15px 0 25px 0;
}
.logo-container img {
    width: 60px;
    margin-right: 15px;
}
.logo-container h2 {
    color: #0b3d0b;
    font-weight: bold;
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

.leaf {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #6b8f71;
    opacity: 0.3;
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
    max-width: 900px;
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
    transition: transform 0.2s;
}
.nav-item img {
    width: 35px;
    margin-bottom: 5px;
}
.nav-item:hover {
    transform: scale(1.1);
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
    st.session_state.price_range = (int(data["price"].min()), int(data["price"].max()))

# ---------------------------
# LOADING SCREEN
# ---------------------------
if not st.session_state.loaded:
    st.markdown("""
    <div class="loader-container">
        <div class="walker"></div>
        <h1 style="color:#0b3d0b; font-size:80px; margin-top:20px;">Rest Quest</h1>
        <p style="color:#0b3d0b; font-size:20px;">Finding your next home...</p>
        <div class="leaf" style="left:10%; animation-delay:0s;"></div>
        <div class="leaf" style="left:30%; animation-delay:1s;"></div>
        <div class="leaf" style="left:50%; animation-delay:2s;"></div>
        <div class="leaf" style="left:70%; animation-delay:1.5s;"></div>
        <div class="leaf" style="left:85%; animation-delay:0.5s;"></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# TOP LOGO
# ---------------------------
st.markdown(f"""
<div class="logo-container">
    <img src="logo.png" alt="Logo">
    <h2>Rest Quest</h2>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# HOME PAGE
# ---------------------------
if st.session_state.page == "Home":
    c_all, c1, c2 = st.columns([1,1,1])
    with c_all:
        if st.button("All", key="all_btn"): st.session_state.filter_type = "All"
    with c1:
        if st.button("🏠 Rent", key="rent_btn"): st.session_state.filter_type = "Rent"
    with c2:
        if st.button("🏷 Sale", key="sale_btn"): st.session_state.filter_type = "Sale"

    st.markdown("---")
    st.header("Recommended Houses")

    filtered = data.copy()
    if st.session_state.filter_type != "All":
        filtered = filtered[filtered["type"] == st.session_state.filter_type]
    filtered = filtered[
        (filtered["price"] >= st.session_state.price_range[0]) &
        (filtered["price"] <= st.session_state.price_range[1])
    ]

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
    
    price_slider = st.slider(
        "Price Range",
        int(data["price"].min()), int(data["price"].max()),
        st.session_state.price_range
    )
    st.session_state.price_range = price_slider

    filtered = data.copy()
    if search_query:
        filtered = filtered[
            filtered["name"].str.contains(search_query, case=False) |
            filtered["location"].str.contains(search_query, case=False)
        ]
    filtered = filtered[
        (filtered["price"] >= st.session_state.price_range[0]) &
        (filtered["price"] <= st.session_state.price_range[1])
    ]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"{row['location']} | 💰 ₱{row['price']:,}")
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
    price_slider_set = st.slider(
        "Select Price Range",
        int(data["price"].min()), int(data["price"].max()),
        st.session_state.price_range
    )
    st.session_state.price_range = price_slider_set

# ---------------------------
# SPACE FOR NAV BAR
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAVIGATION (LOGO + NAME)
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

pages = [("Home", "home.png"), ("Search", "search.png"), ("Settings", "settings.png")]
cols = st.columns(3)
for i, (name, icon) in enumerate(pages):
    with cols[i]:
        if st.button(" ", key=f"nav_{name.lower()}"): st.session_state.page = name
        st.markdown(f'<div class="nav-item"><img src="{icon}"><span>{name}</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
