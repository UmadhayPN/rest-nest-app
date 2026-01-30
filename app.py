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
    padding: 16px 30px;
    border-bottom: 1px solid #ddd;
}

/* CONTENT */
.content {
    margin-top: 90px;
    margin-bottom: 90px;
    padding: 0 40px;
}

/* CARD */
.card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    margin-bottom: 22px;
}

.price {
    font-size: 18px;
    font-weight: 600;
}

/* PAGINATION */
.pagination {
    text-align: center;
    font-weight: 500;
}

/* BOTTOM NAV */
.bottom-nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #FAFAF7;
    border-top: 1px solid #ddd;
    padding: 12px 0;
    z-index: 1000;
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

# FILTER (SAFE — DOES NOT RESET PAGE)
filter_choice = st.radio(
    "",
    ["All", "Rent", "Sale"],
    horizontal=True,
    key="filter"
)

# FILTER DATA
if st.session_state.filter == "All":
    filtered_data = data
else:
    filtered_data = data[data["type"] == st.session_state.filter]

# TOTAL PAGES (AFTER FILTER)
total_pages = max(1, math.ceil(len(filtered_data) / ITEMS_PER_PAGE))

# CLAMP PAGE
st.session_state.page = max(1, min(st.session_state.page, total_pages))

# SLICE DATA (THIS IS THE FIX)
start = (st.session_state.page - 1) * ITEMS_PER_PAGE
end = start + ITEMS_PER_PAGE
page_data = filtered_data.iloc[start:end]

# RENDER ONLY CURRENT PAGE
for _, row in page_data.iterrows():
    st.markdown(f"""
    <div class="card">
        <h4>🏡 {row['name']}</h4>
        <p>📍 {row['location']}</p>
        <p class="price">💰 ₱{int(row['price']):,}</p>
        <p>📌 {row['type']}</p>
    </div>
    """, unsafe_allow_html=True)

# PAGINATION CONTROLS
c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    if st.button("⬅ Prev", disabled=st.session_state.page == 1):
        st.session_state.page -= 1
        st.rerun()

with c2:
    st.markdown(
        f"<div class='pagination'>Page {st.session_state.page} of {total_pages}</div>",
        unsafe_allow_html=True
    )

with c3:
    if st.button("Next ➡", disabled=st.session_state.page == total_pages):
        st.session_state.page += 1
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# BOTTOM NAV
# ----------------------------------
st.markdown("""
<div class="bottom-nav">
    <div style="display:flex; justify-content:space-around;">
        <div>🏠 Home</div>
        <div>🔍 Search</div>
        <div>⚙️ Settings</div>
    </div>
</div>
""", unsafe_allow_html=True)
