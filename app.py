import streamlit as st
import pandas as pd
import math

# ----------------------------------
# CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Rest Quest",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------
# CSS
# ----------------------------------
st.markdown("""
<style>
html, body, [class*="stApp"] {
    background-color: #FAFAF7;
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER */
.header {
    position: fixed;
    top: 0;
    width: 100%;
    background: #FAFAF7;
    z-index: 1000;
    padding: 14px 30px;
    border-bottom: 1px solid #ddd;
}

/* CONTENT */
.content {
    margin-top: 90px;
    margin-bottom: 120px;
    padding: 0 35px;
}

/* CARD */
.card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    margin-bottom: 22px;
}

/* PRICE */
.price {
    font-size: 18px;
    font-weight: 600;
}

/* ANDROID BOTTOM NAV */
.bottom-nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #FAFAF7;
    border-top: 1px solid #ddd;
    padding: 10px 0;
    z-index: 1000;
}

.nav-items {
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 12px;
    color: #888;
}

.nav-item.active {
    color: #2E7D32;
    font-weight: 600;
}

.nav-icon {
    font-size: 22px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# DATA
# ----------------------------------
data = pd.DataFrame({
    "name": [
        "Modern Apartment", "Cozy Studio", "Family House",
        "Luxury Condo", "Budget Room", "City Loft",
        "Suburban Home", "Beachside Stay", "Mountain Cabin"
    ],
    "location": [
        "Manila", "Cebu", "Davao", "BGC",
        "Quezon City", "Makati", "Laguna", "Palawan", "Baguio"
    ],
    "price": [
        15000, 8000, 22000, 45000,
        6000, 18000, 20000, 30000, 12000
    ],
    "type": [
        "Rent", "Rent", "Sale", "Sale",
        "Rent", "Rent", "Sale", "Rent", "Rent"
    ]
})

# ----------------------------------
# SESSION STATE
# ----------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "filter" not in st.session_state:
    st.session_state.filter = "All"

if "tab" not in st.session_state:
    st.session_state.tab = "Home"

ITEMS_PER_PAGE = 3

# ----------------------------------
# HEADER
# ----------------------------------
st.markdown("""
<div class="header">
    <h2>🏠 Rest Quest</h2>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# CONTENT
# ----------------------------------
st.markdown('<div class="content">', unsafe_allow_html=True)

# ---------- HOME TAB ----------
if st.session_state.tab == "Home":

    filter_choice = st.radio(
        "",
        ["All", "Rent", "Sale"],
        horizontal=True,
        key="filter"
    )

    # ✅ FIXED FILTER
    if filter_choice == "All":
        filtered_data = data
    else:
        filtered_data = data[data["type"] == filter_choice]

    total_pages = max(1, math.ceil(len(filtered_data) / ITEMS_PER_PAGE))
    st.session_state.page = max(1, min(st.session_state.page, total_pages))

    start = (st.session_state.page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_data = filtered_data.iloc[start:end]

    for _, row in page_data.iterrows():
        st.markdown(f"""
        <div class="card">
            <h4>🏡 {row['name']}</h4>
            <p>📍 {row['location']}</p>
            <p class="price">💰 ₱{int(row['price']):,}</p>
            <p>📌 {row['type']}</p>
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("⬅ Prev", disabled=st.session_state.page == 1):
            st.session_state.page -= 1
            st.rerun()

    with c2:
        st.markdown(
            f"<div style='text-align:center;'>Page {st.session_state.page} of {total_pages}</div>",
            unsafe_allow_html=True
        )

    with c3:
        if st.button("Next ➡", disabled=st.session_state.page == total_pages):
            st.session_state.page += 1
            st.rerun()

# ---------- SEARCH TAB ----------
elif st.session_state.tab == "Search":
    st.subheader("🔍 Search")
    query = st.text_input("Search by name or location")

    results = data[
        data["name"].str.contains(query, case=False) |
        data["location"].str.contains(query, case=False)
    ] if query else data

    for _, row in results.iterrows():
        st.markdown(f"""
        <div class="card">
            <h4>{row['name']}</h4>
            <p>{row['location']}</p>
            <p class="price">₱{int(row['price']):,}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- SETTINGS TAB ----------
elif st.session_state.tab == "Settings":
    st.subheader("⚙️ Settings")
    st.write("Support: support@restquest.com")
    st.write("Post listing via email")

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# ANDROID BOTTOM NAV
# ----------------------------------
st.markdown(f"""
<div class="bottom-nav">
    <div class="nav-items">

        <div class="nav-item {'active' if st.session_state.tab == 'Home' else ''}">
            <div class="nav-icon">🏠</div>
            Home
        </div>

        <div class="nav-item {'active' if st.session_state.tab == 'Search' else ''}">
            <div class="nav-icon">🔍</div>
            Search
        </div>

        <div class="nav-item {'active' if st.session_state.tab == 'Settings' else ''}">
            <div class="nav-icon">⚙️</div>
            Settings
        </div>

    </div>
</div>
""", unsafe_allow_html=True)

# ✅ FIXED invisible buttons overlay (aligned with nav)
nav_cols = st.columns(3)
with nav_cols[0]:
    if st.button("Home", key="nav_home"):
        st.session_state.tab = "Home"
        st.rerun()
with nav_cols[1]:
    if st.button("Search", key="nav_search"):
        st.session_state.tab = "Search"
        st.rerun()
with nav_cols[2]:
    if st.button("Settings", key="nav_settings"):
        st.session_state.tab = "Settings"
        st.rerun()
