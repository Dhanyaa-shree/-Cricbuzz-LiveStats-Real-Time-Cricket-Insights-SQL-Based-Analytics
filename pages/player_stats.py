import streamlit as st
import http.client
import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# ---------------- LOAD API KEY ----------------
load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")

if not API_KEY:
    st.error("❌ RAPIDAPI_KEY not found in .env file")
    st.stop()

BASE_URL = "cricbuzz-cricket.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": BASE_URL
}

# ---------------- SEARCH PLAYERS (SAFE) ----------------
def search_players(query: str):
    try:
        query = query.strip()

        if not query:
            return {"player": []}

        conn = http.client.HTTPSConnection(BASE_URL)
        endpoint = f"/stats/v1/player/search?plrN={query}"

        conn.request("GET", endpoint, headers=HEADERS)
        res = conn.getresponse()
        data = res.read()
        conn.close()

        result = json.loads(data.decode("utf-8"))

        return result if isinstance(result, dict) else {"player": []}

    except Exception:
        return {"player": []}

# ---------------- PLAYER DETAILS ----------------
def get_player_details(player_id: int):
    try:
        conn = http.client.HTTPSConnection(BASE_URL)
        conn.request("GET", f"/stats/v1/player/{player_id}", headers=HEADERS)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data.decode("utf-8"))
    except:
        return {}

# ---------------- STATS API ----------------
def get_player_stats(player_id: int, stat_type="batting"):
    try:
        url = f"https://{BASE_URL}/stats/v1/player/{player_id}/{stat_type}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        return res.json() if res.status_code == 200 else {}
    except:
        return {}

# ---------------- CONVERT TABLE ----------------
def parse_stats_table(stats_json):
    if not stats_json or "headers" not in stats_json or "values" not in stats_json:
        return pd.DataFrame()

    headers = stats_json["headers"]
    rows = [r["values"] for r in stats_json["values"]]
    return pd.DataFrame(rows, columns=headers)

# ---------------- MAIN FUNCTION (IMPORTANT) ----------------
def show_player_stats():
    st.title("📊 Player Stats & Profile")

    player_name = st.text_input("Enter player name (e.g. Kohli, Dhoni, Smith)")

    if player_name:
        results = search_players(player_name)
        players = results.get("player", [])

        if not players:
            st.warning("⚠ No players found. Try full name like 'Virat Kohli'.")
            return

        selected_name = st.selectbox("Select Player", [p["name"] for p in players])
        selected_player = next(p for p in players if p["name"] == selected_name)

        player_id = selected_player["id"]

        details = get_player_details(player_id)

        tabs = st.tabs(["📌 Profile", "🏏 Batting Stats", "🎯 Bowling Stats"])

        # ---------------- PROFILE ----------------
        with tabs[0]:
            st.subheader(selected_name)
            st.write("Team:", selected_player.get("teamName", "N/A"))

            if "image" in details:
                st.image(details["image"], width=150)

            st.write("Role:", details.get("role", "N/A"))
            st.write("Batting:", details.get("bat", "N/A"))
            st.write("Bowling:", details.get("bowl", "N/A"))

        # ---------------- BATTING ----------------
        with tabs[1]:
            batting = get_player_stats(player_id, "batting")
            df = parse_stats_table(batting)

            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No batting stats available")

        # ---------------- BOWLING ----------------
        with tabs[2]:
            bowling = get_player_stats(player_id, "bowling")
            df = parse_stats_table(bowling)

            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No bowling stats available")