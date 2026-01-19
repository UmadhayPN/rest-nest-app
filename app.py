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

/* ---------- TOP LOGO ---------- */
.logo {
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

/* ---------- LOADING SCREEN ---------- */
.loader-container {
    height: 100vh;
    background: radial-gradient(circle, #0a1a0a, #000);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
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

/* ---------- FALLING LEAVES ---------- */
.leaf {
    position: absolute;
    width: 10px;
    height: 10px;
    background: #00ff00;
    opacity: 0.3;
    animation: fall 5s linear infinite;
}

@keyframes fall {
    0% { transform: translateY(-100px); }
    100% { transform: translateY(100vh); }
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

/* Buttons */
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

if "filter_type" not in st.session_state:
    st.session_state.filter_type = "All"

# ---------------------------
# LOADING SCREEN
# ---------------------------
if not st.session_state.loaded:
    st.markdown("""
    <div class="loader-container">
        <div class="walker"></div>
        <h1>Rest Nest</h1>
        <p>Finding your next home...</p>
        <div class="leaf" style="left:10%"></div>
        <div class="leaf" style="left:40%"></div>
        <div class="leaf" style="left:70%"></div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(3)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# TOP LOGO
# ---------------------------
st.markdown('<div class="logo">🏡 Rest Nest</div>', unsafe_allow_html=True)

# ---------------------------
# HOME PAGE
# ---------------------------
if st.session_state.page == "Home":
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("All"):
            st.session_state.filter_type = "All"
    with col2:
        if st.button("Rent"):
            st.session_state.filter_type = "Rent"
    with col3:
        if st.button("Sale"):
            st.session_state.filter_type = "Sale"

    st.markdown("---")
    st.header("🏠 Recommended Houses")

    filtered = data.copy()
    if st.session_state.filter_type != "All":
        filtered = filtered[filtered["type"] == st.session_state.filter_type]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']}")
        st.write(f"🏷 {row['type']} | 💰 ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SEARCH PAGE
# ---------------------------
elif st.session_state.page == "Search":
    st.header("🔍 Search Houses")

    search_query = st.text_input("Search by name or location")

    location = st.selectbox(
        "Location",
        ["All"] + list(data["location"].unique())
    )

    price_range = st.slider(
        "Price Range",
        int(data["price"].min()),
        int(data["price"].max()),
        (int(data["price"].min()), int(data["price"].max()))
    )

    filtered = data.copy()

    if search_query:
        filtered = filtered[
            filtered["name"].str.contains(search_query, case=False) |
            filtered["location"].str.contains(search_query, case=False)
        ]

    if location != "All":
        filtered = filtered[filtered["location"] == location]

    filtered = filtered[
        (filtered["price"] >= price_range[0]) &
        (filtered["price"] <= price_range[1])
    ]

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"{row['location']} | ₱{row['price']:,}")
        st.markdown("---")

# ---------------------------
# SETTINGS PAGE
# ---------------------------
elif st.session_state.page == "Settings":
    st.header("⚙️ Settings")

    st.subheader("👤 User Profile")
    st.write("Guest User")

    st.subheader("❓ Get Help")
    st.markdown("""
    📧 Email: support@restnest.com  
    📘 [How to Use Rest Nest](https://example.com/instructions)
    """)

    st.subheader("📢 Post Listing")
    st.markdown("""
    Want to post a house for rent or sale?  
    📧 [Send listing via email](mailto:listings@restnest.com)
    """)

# ---------------------------
# SPACE FOR NAV BAR
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAVIGATION
# ---------------------------
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🏠 Home", key="nav_home"):
        st.session_state.page = "Home"

with c2:
    if st.button("🔍 Search", key="nav_search"):
        st.session_state.page = "Search"

with c3:
    if st.button("⚙️ Settings", key="nav_settings"):
        st.session_state.page = "Settings"

st.markdown('</div>', unsafe_allow_html=True)
