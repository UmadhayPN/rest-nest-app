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

/* ---------- TOP HEADER ---------- */
.logo-container {
    position: sticky;
    top: 0;
    background: #fefcf4;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15px;
    border-bottom: 2px solid #0b3d0b;
    z-index: 9999;
}
.logo-container img {
    width: 60px;
    margin-right: 15px;
}
.logo-container h2 {
    margin: 0;
    font-size: 32px;
    font-weight: bold;
}

/* ---------- LOADING SCREEN ---------- */
.loader-container {
    position: fixed;
    inset: 0;
    background: linear-gradient(#e8efe8, #fefcf4);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10000;
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
    width: 14px;
    height: 14px;
    background: #0b3d0b;
    border-radius: 50%;
    position: absolute;
    top: -20px;
    left: 10px;
}
@keyframes walk {
    from { transform: translateX(-30px); }
    to { transform: translateX(30px); }
}

.leaf {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #6b8f71;
    border-radius: 50%;
    opacity: 0.4;
    animation: fall linear infinite;
}
@keyframes fall {
    from { transform: translateY(-100px); }
    to { transform: translateY(100vh); }
}

/* ---------- BOTTOM NAV ---------- */
.nav-container {
    position: sticky;
    bottom: 0;
    background: #fefcf4;
    border-top: 2px solid #0b3d0b;
    display: flex;
    justify-content: center;
    gap: 60px;
    padding: 12px;
    z-index: 9999;
}
.nav-container img {
    width: 48px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("PH_houses_v2.csv")

    df["price"] = (
        df["price"].astype(str)
        .str.replace("₱", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df.dropna(subset=["price"])

data = load_data()

# ---------------------------
# SESSION STATES
# ---------------------------
if "loaded" not in st.session_state:
    st.session_state.loaded = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "home_filter" not in st.session_state:
    st.session_state.home_filter = "All"

if "search_filter" not in st.session_state:
    st.session_state.search_filter = "All"

if "price_range" not in st.session_state:
    st.session_state.price_range = (
        int(data.price.min()),
        int(data.price.max())
    )

# ---------------------------
# LOADING SCREEN
# ---------------------------
if not st.session_state.loaded:
    st.markdown("""
    <div class="loader-container">
        <h1>Rest Quest</h1>
        <div class="walker"></div>
        <div class="leaf" style="left:10%; animation-duration:6s;"></div>
        <div class="leaf" style="left:30%; animation-duration:9s;"></div>
        <div class="leaf" style="left:55%; animation-duration:7s;"></div>
        <div class="leaf" style="left:75%; animation-duration:10s;"></div>
        <div class="leaf" style="left:90%; animation-duration:8s;"></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
<div class="logo-container">
    <img src="image-removebg-preview.png">
    <h2>Rest Quest</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------
# HOME PAGE
# ---------------------------
if st.session_state.page == "Home":

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("All"):
            st.session_state.home_filter = "All"
    with c2:
        if st.button("🏠 Rent"):
            st.session_state.home_filter = "Rent"
    with c3:
        if st.button("🏷 Sale"):
            st.session_state.home_filter = "Sale"

    st.header("Recommended Houses")

    df = data.copy()
    if st.session_state.home_filter != "All":
        df = df[df["type"] == st.session_state.home_filter]

    for _, r in df.iterrows():
        st.subheader(r["name"])
        st.write(f"📍 {r['location']}")
        st.write(f"💰 ₱{int(r['price']):,}")
        st.markdown("---")

# ---------------------------
# SEARCH PAGE
# ---------------------------
elif st.session_state.page == "Search":

    st.header("Search Houses")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("All", key="s_all"):
            st.session_state.search_filter = "All"
    with c2:
        if st.button("🏠 Rent", key="s_rent"):
            st.session_state.search_filter = "Rent"
    with c3:
        if st.button("🏷 Sale", key="s_sale"):
            st.session_state.search_filter = "Sale"

    st.session_state.price_range = st.slider(
        "Price Range (₱)",
        int(data.price.min()),
        int(data.price.max()),
        st.session_state.price_range,
        step=1000
    )

    query = st.text_input("Search by name or location")

    df = data.copy()

    if query:
        df = df[
            df.name.str.contains(query, case=False) |
            df.location.str.contains(query, case=False)
        ]

    if st.session_state.search_filter != "All":
        df = df[df.type == st.session_state.search_filter]

    df = df[
        (df.price >= st.session_state.price_range[0]) &
        (df.price <= st.session_state.price_range[1])
    ]

    for _, r in df.iterrows():
        st.subheader(r["name"])
        st.write(f"📍 {r['location']} | 💰 ₱{int(r['price']):,}")
        st.markdown("---")

# ---------------------------
# SETTINGS PAGE
# ---------------------------
elif st.session_state.page == "Settings":

    st.header("Settings")

    st.subheader("Help")
    st.markdown("""
📧 support@restquest.com  
📘 [How to Use Rest Quest](https://example.com)
""")

    st.subheader("Post a Listing")
    st.markdown("""
📧 listings@restquest.com  
📄 [Posting Instructions](https://example.com/posting)
""")

# ---------------------------
# BOTTOM NAV
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button(" ", key="nav_home"):
        st.session_state.page = "Home"
    st.markdown('<img src="Home.png">', unsafe_allow_html=True)

with c2:
    if st.button(" ", key="nav_search"):
        st.session_state.page = "Search"
    st.markdown('<img src="Search.png">', unsafe_allow_html=True)

with c3:
    if st.button(" ", key="nav_settings"):
        st.session_state.page = "Settings"
    st.markdown('<img src="Settings.png">', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
