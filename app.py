import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Nest", layout="wide")

# ---------------------------
# CSS (ANDROID-STYLE NAV)
# ---------------------------
st.markdown("""
<style>
body {
    background-color: white;
    color: black;
}

/* Bottom navigation container */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 65px;
    background-color: #ffffff;
    border-top: 1px solid #ccc;
    display: flex;
    justify-content: space-around;
    align-items: center;
    z-index: 999;
}

/* Make Streamlit buttons look like nav buttons */
.bottom-nav button {
    background: none !important;
    border: none !important;
    font-size: 16px !important;
    color: black !important;
    font-weight: 500;
}

/* Remove Streamlit button padding */
div.stButton > button {
    padding: 0.5rem 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------
# LOADING SCREEN
# ---------------------------
if not st.session_state.loaded:
    st.markdown(
        "<h1 style='text-align:center; margin-top:200px;'>Rest Nest</h1>",
        unsafe_allow_html=True
    )
    time.sleep(2)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# LOGIN SCREEN (NO NAV)
# ---------------------------
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>Login</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------------------
# MAIN CONTENT
# ---------------------------
if st.session_state.page == "Home":
    st.header("🏠 Recommended Houses")

    for _, row in data.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']}")
        st.write(f"🏷 {row['type']} | ₱{row['price']:,}")
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

    for _, row in filtered.iterrows():
        st.subheader(row["name"])
        st.write(f"{row['location']} | {row['type']} | ₱{row['price']:,}")
        st.markdown("---")

elif st.session_state.page == "Settings":
    st.header("⚙️ Settings")

    st.subheader("👤 Profile")
    st.write("Username: admin")
    st.write("Email: admin@restnest.com")

    if st.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()

# ---------------------------
# CONTENT SPACER
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# ANDROID-STYLE BOTTOM NAV
# ---------------------------
st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠\nHome"):
        st.session_state.page = "Home"

with col2:
    if st.button("🔍\nSearch"):
        st.session_state.page = "Search"

with col3:
    if st.button("⚙️\nSettings"):
        st.session_state.page = "Settings"

st.markdown('</div>', unsafe_allow_html=True)
