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
    color: #000000;
}

/* HEADER */
.header {
    position: fixed;
    top: 0;
    width: 100%;
    background: #FAFAF7;
    z-index: 1000;
    padding: 40px 30px;
    border-bottom: 1px solid #ddd;
    color: #000000;
}

/* CONTENT */
.content {
    margin-top: 140px;
    margin-bottom: 120px;
    padding: 0 35px;
    color: #000000;
}

/* CARD */
.card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    margin-bottom: 22px;
    color: #000000;
}

/* PRICE */
.price {
    font-size: 18px;
    font-weight: 600;
    color: #000000;
}

/* RADIO GROUP BACKGROUND */
div[role="radiogroup"] {
    background-color: #f5f5dc;   /* ✅ beige background */
    padding: 10px;
    border-radius: 12px;
    display: inline-block;
}

/* RADIO BUTTONS */
div[role="radiogroup"] > label {
    display: inline-block;
    background: #f5f5dc;         /* ✅ beige button background */
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 6px 16px;
    margin-right: 8px;
    cursor: pointer;
    font-weight: 500;
    color: #000000;
}

div[role="radiogroup"] > label:hover {
    background: #e5e5c4;         /* darker beige on hover */
}

div[role="radiogroup"] input:checked + div {
    background: #e5e5c4;         /* selected beige */
    color: #000000;
    border: 1px solid #b5b59c;
    border-radius: 20px;
    padding: 6px 16px;
}

/* BUTTONS (Next + Bottom Nav) */
button[kind="primary"], div.stButton > button {
    background-color: #f5f5dc !important;  /* ✅ beige */
    color: #000000 !important;
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
}
button[kind="primary"]:hover, div.stButton > button:hover {
    background-color: #e5e5c4 !important;  /* darker beige on hover */
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# LOAD DATASET
# ----------------------------------
data = pd.read_csv("PH_houses_v2.csv")

if "price" in data.columns:
    data["price"] = (
        data["price"]
        .astype(str)
        .str.replace(r"[^0-9]", "", regex=True)
        .replace("", "0")
        .astype(int)
    )
else:
    st.error("CSV must contain a 'price' column.")
    st.stop()

# ----------------------------------
# SESSION STATE INITIALIZATION
# ----------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1
if "tab" not in st.session_state:
    st.session_state.tab = "Home"
if "filter_type" not in st.session_state:
    st.session_state.filter_type = "All"
if "price_range" not in st.session_state:
    st.session_state.price_range = (data['price'].min(), data['price'].max())

ITEMS_PER_PAGE = 10

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
        "🏷️ Filter listings by type",
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
            <p class="price">💰 ₱{row['price']:,}</p>
            <p>📌 {row['type']}</p>
            <p>🛁 Bathrooms: {row['bathrooms']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Pagination
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

    # ✅ Price slider
    price_min, price_max = int(data['price'].min()), int(data['price'].max())
    st.session_state.price_range = st.slider(
        "💰 Select price range",
        min_value=price_min,
        max_value=price_max,
        value=(price_min, price_max),
        step=10000
    )

    # Apply filters
    results = data[
        (data["price"] >= st.session_state.price_range[0]) &
        (data["price"] <= st.session_state.price_range[1]) &
        (
            data["name"].str.contains(query, case=False) |
            data["location"].str.contains(query, case=False)
        )
    ] if query else data[
        (data["price"] >= st.session_state.price_range[0]) &
        (data["price"] <= st.session_state.price_range[1])
    ]

    # ✅ Pagination for Search
    total_pages = max(1, math.ceil(len(results) / ITEMS_PER_PAGE))
    st.session_state.page = max(1, min(st.session_state.page, total_pages))

    start = (st.session_state.page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_results = results.iloc[start:end]

    for _, row in page_results.iterrows():
        st.markdown(f"""
        <div class="card">
            <h4>{row['name']}</h4>
            <p>{row['location']}</p>
            <p class="price">₱{row['price']:,}</p>
            <p>📌 {row['type']}</p>
            <p>🛁 Bathrooms: {row['bathrooms']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Pagination controls for Search
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
