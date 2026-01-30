import streamlit as st
import pandas as pd
import math
# ----------------------------------
# LOAD DATASET
# ----------------------------------
# ✅ Load your actual dataset
data = pd.read_csv("PH_houses_v2.csv")

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
</style>
""", unsafe_allow_html=True)


# Expecting columns like: name, location, price, type
# If column names differ, adjust accordingly

# ----------------------------------
# SESSION STATE
# ----------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "tab" not in st.session_state:
    st.session_state.tab = "Home"

ITEMS_PER_PAGE = 10  # ✅ Show 10 houses per page

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
        horizontal=True
    )

    if filter_choice == "All":
        filtered_data = data
    else:
        filtered_data = data[data["type"].str.lower() == filter_choice.lower()]

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

    # Pagination controls
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
# SIMPLE BOTTOM NAV
# ----------------------------------
nav_cols = st.columns(3)
with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.tab = "Home"
        st.rerun()
with nav_cols[1]:
    if st.button("🔍 Search", use_container_width=True):
        st.session_state.tab = "Search"
        st.rerun()
with nav_cols[2]:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.tab = "Settings"
        st.rerun()

