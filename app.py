import streamlit as st

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

# ----------------------------
# GLOBAL CSS
# ----------------------------
st.markdown("""
<style>

/* PASTEL BACKGROUND FOR ENTIRE APP */
.stApp {
    background: linear-gradient(135deg, #fdf6ec, #fff8f2);
}

/* REMOVE TOP SPACE */
.block-container {
    padding-top: 0.5rem !important;
}

/* REMOVE LINE */
hr {
    display: none;
}

/* RED HEADER BOX */
.logo-container {
    background: linear-gradient(135deg, #8B0000, #cc0000);
    padding: 15px 10px;
    border-radius: 12px;
    margin: 10px auto;
    text-align: center;
    max-width: 600px;
}

/* LOGO */
.logo-container img {
    max-width: 220px;
    height: auto;
    margin-bottom: 10px;
}

/* BIG CENTER TEXT */
.logo-subtitle {
    color: red;
    font-size: 22px;
    font-weight: 700;
    text-align: center;
}

/* OPTIONAL: SOFT CARD STYLE TO MATCH PASTEL THEME */
div[data-testid="stMetric"],
div[data-testid="stInfoBox"],
.stAlert {
    background-color: #ffffffcc;
    border-radius: 10px;
    border: 1px solid #f0f0f0;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown('<div class="logo-container">', unsafe_allow_html=True)

st.image("logo.png")

st.markdown(
    '<div class="logo-subtitle">🏏 Cricbuzz LiveStats: Real-time Cricket Insights</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
# ----------------------------
page = st.sidebar.radio(
    "🏏 Navigation",
    ["🏠 Home", "⚡ Live Matches", "📊 Top Stats", "🔍 SQL Analytics", "🛠️ CRUD"]
)

# ----------------------------
# HOME
# ----------------------------
def show_home():
    st.subheader("Dashboard Features")

    col1, col2, col3, col4 = st.columns(4)

    col1.info("⚡ Live Matches")
    col2.info("📊 Top Stats")
    col3.info("🔍 SQL Analytics")
    col4.info("🛠️ CRUD Operations")

# ----------------------------
# SAFE IMPORT
# ----------------------------
def safe_run(module, func):
    try:
        m = __import__(module, fromlist=[func])
        getattr(m, func)()
    except Exception as e:
        st.error(f"Error: {e}")

# ----------------------------
# ROUTING
# ----------------------------
if page == "🏠 Home":
    show_home()

elif page == "⚡ Live Matches":
    safe_run("pages.live_matches", "show_live_matches")

elif page == "📊 Top Stats":
    safe_run("pages.player_stats", "show_player_stats")

elif page == "🔍 SQL Analytics":
    safe_run("pages.sql_queries", "show_sql_queries")

elif page == "🛠️ CRUD":
    safe_run("pages.crud_operations", "show_crud_operations")