import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Nest", layout="wide")

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
body {
    background-color: black;
    color: #00ff00;
}

/* ---------- LOADING ANIMATION ---------- */
.loader-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.walker {
    width: 40px;
    height: 80px;
    border: 3px solid #00ff00;
    border-radius: 20px;
    position: relative;
    animation: walk 1s infinite alternate;
}

.walker::before {
    content: '';
    width: 12px;
    height: 12px;
    background: #00ff00;
    border-radius: 50%;
    position: absolute;
    top: -18px;
    left: 11px;
}

@keyframes walk {
    0% { transform: translateX(-20px); }
    100% { transform: translateX(20px); }
}

/* ---------- FIXED BOTTOM NAV ---------- */
.nav-container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #111;
    padding: 10px 0;
    border-top: 1px solid #333;
    z-index: 1000;
}

/* Make buttons full width */
div.stButton > button {
    width: 100%;
    background-color: transparent;
    color: #00ff00;
    border: none;
    font-size: 16px;
}

div.stButton > button:hover {
    color: white;
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

# ---------------------------
# LOADING SCREEN (WITH ANIMATION)
# ---------------------------
if not st.session_state.loaded:
    st.markdown("""
    <div class="loader-container">
        <div class="walker"></div>
        <h1>Rest Nest</h1>
        <p>Finding your next home...</p>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(3)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# MAIN CONTENT
# ---------------------------
if st.session_state.page == "Home":
    st.header("🏠 Recommended Houses")

    for _, row in data.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 Location: {row['location']}")
        st.write(f"🏷 Type: {row['type']}")
        st.write(f"💰 Price: ₱{row['price']:,}")
        st.markdown("---")

elif st.session_state.page == "Search":
    st.header("🔍 Search Houses")

    location = st.selectbox(
        "Location",
        ["All"] + list(data["location"].unique())
    )

    house_type = st.selectbox(
        "Type",
        ["All", "Rent", "Sale"]
    )

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

elif st.session_state.page == "Settings":
    st.header("⚙️ Settings")

    st.subheader("👤 User Profile")
    st.write("Guest User")

    st.subheader("❓ Get Help")
    st.write("support@restnest.com")

# ---------------------------
# SPACE SO CONTENT IS NOT COVERED
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# FIXED BOTTOM NAVIGATION
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", key="nav_home"):
        st.session_state.page = "Home"

with col2:
    if st.button("🔍 Search", key="nav_search"):
        st.session_state.page = "Search"

with col3:
    if st.button("⚙️ Settings", key="nav_settings"):
        st.session_state.page = "Settings"

st.markdown('</div>', unsafe_allow_html=True)
