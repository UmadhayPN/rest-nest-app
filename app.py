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
}

/* ---------- TOP LOGO ---------- */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 15px 0 25px 0;
}
.logo-container img {
    width: 50px;
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
.loader-container h1 {
    font-size: 60px;
    color: #0b3d0b;
    margin: 20px 0;
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

.city, .tree {
    position: absolute;
    bottom: 0;
}
.city { width: 50px; height: 60px; background: #0b3d0b; margin: 0 5px; display: inline-block;}
.tree { width: 20px; height: 40px; background: #145214; margin: 0 5px; display: inline-block; }

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
    cursor: pointer;
}
.nav-item img {
    width: 40px;
    margin-bottom: 5px;
    transition: transform 0.2s;
}
.nav-item img:hover {
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
        <div class="walker"></div>
        <h1>Rest Quest</h1>
        <p>Finding your next home...</p>
        <div class="city" style="left:20%"></div>
        <div class="city" style="left:30%"></div>
        <div class="tree" style="left:40%"></div>
        <div class="tree" style="left:50%"></div>
        <div class="leaf" style="left:15%"></div>
        <div class="leaf" style="left:45%"></div>
        <div class="leaf" style="left:75%"></div>
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
    cols = st.columns(3)
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
    st.header("Search Houses")
    search_query = st.text_input("Search by name or location")
    location_filter = st.selectbox("Location", ["All"] + list(data["location"].unique()))
    type_filter = st.selectbox("Type", ["All", "Rent", "Sale"])
    price_range = st.slider("Price Range", int(data["price"].min()), int(data["price"].max()), (int(data["price"].min()), int(data["price"].max())))

    filtered = data.copy()
    if search_query:
        filtered = filtered[
            filtered["name"].str.contains(search_query, case=False) |
            filtered["location"].str.contains(search_query, case=False)
        ]
    if location_filter != "All":
        filtered = filtered[filtered["location"] == location_filter]
    if type_filter != "All":
        filtered = filtered[filtered["type"] == type_filter]
    filtered = filtered[
        (filtered["price"] >= price_range[0]) &
        (filtered["price"] <= price_range[1])
    ]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"{row['location']} | {row['type']} | 💰 ₱{row['price']:,}")
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
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAVIGATION
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
cols = st.columns(3)

nav_items = [
    ("Home", "home.png"),
    ("Search", "search.png"),
    ("Settings", "settings.png")
]

for i, (name, icon) in enumerate(nav_items):
    with cols[i]:
        if st.button("", key=f"nav_{name.lower()}"):
            st.session_state.page = name
        st.markdown(f'<div class="nav-item"><img src="{icon}" alt="{name}"><span>{name}</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
