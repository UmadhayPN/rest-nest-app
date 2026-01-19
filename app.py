import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Nest", layout="wide")

# ---------------------------
# CUSTOM CSS (THEME + ANIMATION + BOTTOM NAV)
# ---------------------------
st.markdown("""
<style>
body {
    background-color: black;
    color: #00ff00;
}

input {
    background-color: #111 !important;
    color: #00ff00 !important;
}

/* -------- LOADING ANIMATION -------- */
.loader-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.walker {
    width: 60px;
    height: 120px;
    border: 3px solid #00ff00;
    border-radius: 30px;
    position: relative;
    animation: walk 1s infinite alternate;
}

.walker::before {
    content: "";
    width: 12px;
    height: 40px;
    background: #00ff00;
    position: absolute;
    bottom: -40px;
    left: 12px;
    animation: leg 0.5s infinite alternate;
}

.walker::after {
    content: "";
    width: 12px;
    height: 40px;
    background: #00ff00;
    position: absolute;
    bottom: -40px;
    right: 12px;
    animation: leg 0.5s infinite alternate-reverse;
}

@keyframes walk {
    from { transform: translateX(-10px); }
    to { transform: translateX(10px); }
}

@keyframes leg {
    from { transform: rotate(10deg); }
    to { transform: rotate(-10deg); }
}

/* -------- BOTTOM NAV -------- */
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

.nav-container button {
    background: none;
    border: none;
    color: #00ff00;
    font-size: 16px;
    cursor: pointer;
}

.nav-container button:hover {
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
# SESSION STATE
# ---------------------------
if "loaded" not in st.session_state:
    st.session_state.loaded = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------
# LOADING SCREEN WITH ANIMATION
# ---------------------------
if not st.session_state.loaded:
    st.markdown("""
    <div class="loader-container">
        <h1>Rest Nest</h1>
        <div class="walker"></div>
        <p>Finding your perfect home...</p>
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

    location = st.selectbox("Location", ["All"] + list(data["location"].unique()))
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

elif st.session_state.page == "Settings":
    st.header("⚙️ Settings")

    st.subheader("👤 Profile")
    st.write("Username: Guest")
    st.write("Email: guest@restnest.com")

    st.subheader("❓ Get Help")
    st.write("support@restnest.com")

# ---------------------------
# SPACE FOR FIXED NAV
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAVIGATION
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
