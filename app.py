import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Nest", layout="wide")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("houses.csv")

data = load_data()

# ---------------------------
# SESSION STATE INIT
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
    st.markdown("<h1 style='text-align:center; margin-top:200px;'>Rest Nest</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# LOGIN SCREEN
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
            st.error("Invalid username or password")

    st.stop()  # Stop execution until logged in

# ---------------------------
# MAIN CONTENT
# ---------------------------
if st.session_state.page == "Home":
    st.header("🏠 Recommended Houses")
    for _, row in data.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']} | {row['type']} | ₱{row['price']:,}")
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
    st.write("Username: admin")
    st.write("Email: admin@restnest.com")

    st.subheader("🚪 Log Out")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()

# ---------------------------
# SPACER TO PUSH NAV TO BOTTOM
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# ANDROID-STYLE BOTTOM NAV
# ---------------------------
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

with nav_col2:
    if st.button("🔍 Search", use_container_width=True):
        st.session_state.page = "Search"

with nav_col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "Settings"
import streamlit as st
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Rest Nest", layout="wide")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("houses.csv")

data = load_data()

# ---------------------------
# SESSION STATE INIT
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
    st.markdown("<h1 style='text-align:center; margin-top:200px;'>Rest Nest</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.loaded = True
    st.rerun()

# ---------------------------
# LOGIN SCREEN
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
            st.error("Invalid username or password")

    st.stop()  # Stop execution until logged in

# ---------------------------
# MAIN CONTENT
# ---------------------------
if st.session_state.page == "Home":
    st.header("🏠 Recommended Houses")
    for _, row in data.iterrows():
        st.subheader(row["name"])
        st.write(f"📍 {row['location']} | {row['type']} | ₱{row['price']:,}")
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
    st.write("Username: admin")
    st.write("Email: admin@restnest.com")

    st.subheader("🚪 Log Out")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()

# ---------------------------
# SPACER TO PUSH NAV TO BOTTOM
# ---------------------------
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# ANDROID-STYLE BOTTOM NAV
# ---------------------------
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

with nav_col2:
    if st.button("🔍 Search", use_container_width=True):
        st.session_state.page = "Search"

with nav_col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "Settings"
