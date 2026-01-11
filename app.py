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

/* Bottom navigation bar */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #111;
    padding: 12px 0;
    display: flex;
    justify-content: space-around;
    border-top: 1px solid #333;
    z-index: 1000;
}

.bottom-nav button {
    background: none;
    border: none;
    color: #00ff00;
    font-size: 18px;
    cursor: pointer;
}

.bottom-nav button:hover {
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
# LOADING SCREEN
# ---------------------------
if "loaded" not in st.session_state:
    st.session_state.loaded = False

if not st.session_state.loaded:
    st.markdown(
        "<h1 style='text-align:center; margin-top:200px;'>Rest Nest</h1>",
        unsafe_allow_html=True
    )
    time.sleep(2)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# PAGE STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------
# HANDLE BOTTOM NAV CLICKS
# ---------------------------
query_params = st.query_params
if "nav" in query_params:
    st.session_state.page = query_params["nav"]

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

    st.subheader("🚪 Log Out")
    if st.button("Log Out"):
        st.session_state.loaded = False
        st.rerun()

# ---------------------------
# SPACE FOR BOTTOM NAV
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAVIGATION BAR
# ---------------------------
st.markdown("""
<div class="bottom-nav">
    <form>
        <button name="nav" value="Home">🏠 Home</button>
        <button name="nav" value="Search">🔍 Search</button>
        <button name="nav" value="Settings">⚙️ Settings</button>
    </form>
</div>
""", unsafe_allow_html=True)
