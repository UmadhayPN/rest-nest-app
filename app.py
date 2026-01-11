import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Nest", layout="wide")

# ---------------------------
# LOAD DATASET
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("houses.csv")

data = load_data()

# ---------------------------
# LOADING SCREEN
# ---------------------------
if "loaded" not in st.session_state:
    st.session_state.loaded = False

if not st.session_state.loaded:
    st.markdown(
        """
        <style>
        body {
            background-color: black;
        }
        </style>
        <h1 style='color: #00ff00; text-align: center; margin-top: 200px;'>
            Rest Nest
        </h1>
        """,
        unsafe_allow_html=True
    )
    time.sleep(2)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# BOTTOM NAVIGATION
# ---------------------------
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    home_btn = st.button("🏠 Home")

with col2:
    search_btn = st.button("🔍 Search")

with col3:
    settings_btn = st.button("⚙️ Settings")

if "page" not in st.session_state:
    st.session_state.page = "Home"

if home_btn:
    st.session_state.page = "Home"
elif search_btn:
    st.session_state.page = "Search"
elif settings_btn:
    st.session_state.page = "Settings"

# ---------------------------
# HOME PAGE
# ---------------------------
if st.session_state.page == "Home":
    st.header("🏠 Recommended Houses")

    for _, row in data.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 Location: {row['location']}")
        st.write(f"🏷 Type: {row['type']}")
        st.write(f"💰 Price: ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SEARCH PAGE
# ---------------------------
elif st.session_state.page == "Search":
    st.header("🔍 Search Houses")

    location = st.selectbox("Select Location", ["All"] + list(data["location"].unique()))
    house_type = st.selectbox("Type", ["All", "Rent", "Sale"])
    price_range = st.slider(
        "Price Range",
        int(data["price"].min()),
        int(data["price"].max()),
        (int(data["price"].min()), int(data["price"].max()))
    )

    filtered = data.copy()

    if location != "All":
        filtered = filtered[filtered["location"] == location]

    if house_type != "All":
        filtered = filtered[filtered["type"] == house_type]

    filtered = filtered[
        (filtered["price"] >= price_range[0]) &
        (filtered["price"] <= price_range[1])
    ]

    st.write(f"### {len(filtered)} results found")

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"{row['location']} | {row['type']} | ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SETTINGS PAGE
# ---------------------------
elif st.session_state.page == "Settings":
    st.header("⚙️ Settings")

    st.subheader("👤 User / Host Profile")
    st.write("Name: Guest User")
    st.write("Role: Viewer")

    st.subheader("❓ Get Help")
    st.write("Email: support@restnest.com")
    st.write("FAQs coming soon")

    st.subheader("🚪 Log Out")
    if st.button("Log Out"):
        st.session_state.loaded = False
        st.rerun()

