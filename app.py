import streamlit as st
import pandas as pd
import math

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Rest Quest",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# GLOBAL STYLES
# -------------------------------
st.markdown("""
<style>
html, body, [class*="stApp"] {
    background-color: #FAFAF7;
    font-family: 'Segoe UI', sans-serif;
}

/* FIXED HEADER */
.header {
    position: fixed;
    top: 0;
    width: 100%;
    background: #FAFAF7;
    z-index: 1000;
    padding: 12px 24px;
    border-bottom: 1px solid #ddd;
}

/* FIXED BOTTOM NAV */
.bottom-nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #FAFAF7;
    border-top: 1px solid #ddd;
    padding: 10px 0;
    z-index: 1000;
}

/* CONTENT AREA */
.content {
    margin-top: 90px;
    margin-bottom: 90px;
    padding: 0 40px;
}

/* HOUSE CARD */
.card {
    background: white;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* PRICE */
.price {
    font-size: 18px;
    font-weight: bold;
    color: #444;
}

/* PAGINATION */
.pagination {
    text-align: center;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SAMPLE DATA (SAFE)
# -------------------------------
data = pd.DataFrame({
    "name": [
        "Modern Apartment",
        "Cozy Studio",
        "Family House",
        "Luxury Condo",
        "Budget Room",
        "City Loft",
        "Suburban Home",
        "Beachside Stay"
    ],
    "location": [
        "Manila", "Cebu", "Davao", "BGC",
        "Quezon City", "Makati", "Laguna", "Palawan"
    ],
    "price": [
        15000, 8000, 22000, 45000,
        6000, 18000, 20000, 30000
    ],
    "type": [
        "Rent", "Rent", "Sale", "Sale",
        "Rent", "Rent", "Sale", "Rent"
    ]
})

# -------------------------------
# SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

ITEMS_PER_PAGE = 3
total_pages = math.ceil(len(data) / ITEMS_PER_PAGE)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<div class="header">
    <h2>🏠 Rest Quest</h2>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# CONTENT
# -------------------------------
st.markdown('<div class="content">', unsafe_allow_html=True)

# FILTER TABS
filter_choice = st.radio(
    "",
    ["All", "Rent", "Sale"],
    horizontal=True
)

filtered_data = data if filter_choice == "All" else data[data["type"] == filter_choice]

# PAGINATION SLICE
start = (st.session_state.page - 1) * ITEMS_PER_PAGE
end = start + ITEMS_PER_PAGE
page_data = filtered_data.iloc[start:end]

# HOUSE CARDS
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
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅ Prev") and st.session_state.page > 1:
        st.session_state.page -= 1

with col2:
    st.markdown(
        f"<div class='pagination'>Page {st.session_state.page} of {total_pages}</div>",
        unsafe_allow_html=True
    )

with col3:
    if st.button("Next ➡") and st.session_state.page < total_pages:
        st.session_state.page += 1

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# BOTTOM NAVIGATION
# -------------------------------
st.markdown("""
<div class="bottom-nav">
    <div style="display:flex; justify-content:space-around;">
        <div>🏠 Home</div>
        <div>🔍 Search</div>
        <div>⚙️ Settings</div>
    </div>
</div>
""", unsafe_allow_html=True)
