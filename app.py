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
# SESSION STATE
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

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Log In"):
        if user == "admin" and pw == "1234":
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
    for _, r in data.iterrows():
        st.subheader(r["name"])
        st.write(f"{r['location']} | {r['type']} | ₱{r['price']:,}")
        st.markdown("---")

elif st.session_state.page == "Search":
    st.header("🔍 Search Houses")

    loc = st.selectbox("Location", ["All"] + list(data["location"].unique()))
    typ = st.selectbox("Type", ["All", "Rent", "Sale"])

    pr = st.slider(
        "Price Range",
        int(data["price"].min()),
        int(data["price"].max()),
        (int(data["price"].min()), int(data["price"].max()))
    )

    f = data.copy()
    if loc != "All":
        f = f[f["location"] == loc]
    if typ != "All":
        f = f[f["type"] == typ]

    f = f[(f["price"] >= pr[0]) & (f["price"] <= pr[1])]

    for _, r in f.iterrows():
        st.subheader(r["name"])
        st.write(f"{r['location']} | {r['type']} | ₱{r['price']:,}")
        st.markdown("---")

elif st.session_state.page == "Settings":
    st.header("⚙️ Settings")
    st.write("Username: admin")
    st.write("Email: admin@restnest.com")

    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()

# ---------------------------
# PUSH NAV TO BOTTOM
# ---------------------------
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

# ---------------------------
# BOTTOM NAV (STABLE)
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

with col2:
    if st.button("🔍 Search", use_container_width=True):
        st.session_state.page = "Search"

with col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "Settings"
