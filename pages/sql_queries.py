import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# ----------------- DB CONNECTION -----------------
def create_connection():
    load_dotenv()

    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "cricbuzz"),
            port=int(os.getenv("DB_PORT", 3307))
        )

        if conn.is_connected():
            return conn

    except Error as e:
        st.error(f"❌ DB Connection Error: {e}")
        return None


# ----------------- RUN QUERY -----------------
def run_query(conn, query):
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"❌ Query Error: {e}")
        return None


# ----------------- SQL QUERIES (FIXED FOR YOUR DB) -----------------
QUERIES = {

# PLAYERS
"1. All Players": """
    SELECT player_name, country, role, batting_style, bowling_style
    FROM players;
""",

"2. Players by Role": """
    SELECT role, COUNT(*) AS total_players
    FROM players
    GROUP BY role;
""",

# TEAMS
"3. All Teams": """
    SELECT * FROM teams;
""",

# VENUES
"4. Venues by Capacity": """
    SELECT venue_name, city, country, capacity
    FROM venues
    ORDER BY capacity DESC;
""",

# MATCHES
"5. All Matches": """
    SELECT * FROM matches;
""",

"6. Match Results": """
    SELECT match_title, match_status, win_margin, player_of_match
    FROM matches;
""",

# BATTING STATS
"7. Top Batting Performances": """
    SELECT p.player_name, b.runs, b.balls_faced, b.strike_rate
    FROM batting_stats b
    JOIN players p ON b.player_id = p.player_id
    ORDER BY b.runs DESC;
""",

"8. Highest Score": """
    SELECT MAX(runs) AS highest_score
    FROM batting_stats;
""",

"9. Avg Runs per Player": """
    SELECT p.player_name, AVG(b.runs) AS avg_runs
    FROM batting_stats b
    JOIN players p ON b.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY avg_runs DESC;
""",

# BOWLING STATS
"10. Top Wicket Takers": """
    SELECT p.player_name, SUM(b.wickets) AS total_wickets
    FROM bowling_stats b
    JOIN players p ON b.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_wickets DESC;
""",

"11. Best Economy Bowlers": """
    SELECT p.player_name, AVG(b.economy_rate) AS economy_rate
    FROM bowling_stats b
    JOIN players p ON b.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY economy_rate ASC;
""",

# CAREER STATS
"12. Career Summary": """
    SELECT p.player_name, c.matches, c.runs, c.wickets,
           c.batting_average, c.batting_strike_rate
    FROM career_stats c
    JOIN players p ON c.player_id = p.player_id;
""",

"13. Top Career Run Scorers": """
    SELECT p.player_name, c.runs
    FROM career_stats c
    JOIN players p ON c.player_id = p.player_id
    ORDER BY c.runs DESC;
""",

"14. Top Career Wicket Takers": """
    SELECT p.player_name, c.wickets
    FROM career_stats c
    JOIN players p ON c.player_id = p.player_id
    ORDER BY c.wickets DESC;
"""

}


# ----------------- STREAMLIT UI -----------------
def show_sql_queries():

    st.title("🏏 Cricket SQL Analytics Dashboard")
    st.markdown("---")

    st.info("Make sure MySQL is running (XAMPP / WAMP) and DB 'cricbuzz' exists")

    conn = create_connection()

    if conn is None:
        st.warning("❌ Database not connected")
        return

    query_name = st.selectbox("Select Query", list(QUERIES.keys()))

    query = st.text_area("SQL Query", QUERIES[query_name], height=200)

    if st.button("Run Query"):

        df = run_query(conn, query)

        if df is not None and not df.empty:
            st.success("Query executed successfully")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No data found or query failed")

    conn.close()