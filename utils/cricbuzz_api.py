import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")


# 🔴 LIVE MATCHES
def get_live_matches():
    conn = http.client.HTTPSConnection(API_HOST)

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }

    try:
        conn.request("GET", "/matches/v1/live", headers=headers)
        res = conn.getresponse()
        data = res.read()

        json_data = json.loads(data)
        matches = []

        for match_type in json_data.get("typeMatches", []):
            for series in match_type.get("seriesMatches", []):
                wrapper = series.get("seriesAdWrapper")
                if not wrapper:
                    continue

                for match in wrapper.get("matches", []):
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})

                    status = info.get("status", "").lower()

                    # ✅ ONLY LIVE MATCHES
                    if "live" in status or "progress" in status:

                        def get_score(team_key):
                            innings = score.get(team_key, {}).get("inngs1", {})
                            if innings:
                                return f"{innings.get('runs',0)}/{innings.get('wickets',0)} ({innings.get('overs',0)})"
                            return "Yet to bat"

                        matches.append({
                            "match_id": info.get("matchId"),
                            "team1": info.get("team1", {}).get("teamName"),
                            "team2": info.get("team2", {}).get("teamName"),
                            "score1": get_score("team1Score"),
                            "score2": get_score("team2Score"),
                            "status": info.get("status"),
                            "venue": info.get("venueInfo", {}).get("ground", "Unknown")
                        })

        return matches

    except Exception as e:
        print("Live Match Error:", e)
        return []


# 📊 SCORECARD
def get_scorecard(match_id):
    conn = http.client.HTTPSConnection(API_HOST)

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }

    try:
        endpoint = f"/mcenter/v1/{match_id}/scard"
        conn.request("GET", endpoint, headers=headers)

        res = conn.getresponse()
        data = res.read()

        json_data = json.loads(data)
        scorecard = []

        for inning in json_data.get("scoreCard", []):
            batting = []
            bowling = []

            # 🏏 Batting
            for bat in inning.get("batTeamDetails", {}).get("batsmenData", {}).values():
                batting.append({
                    "Batsman": bat.get("batName"),
                    "Runs": bat.get("runs"),
                    "Balls": bat.get("balls"),
                    "4s": bat.get("fours"),
                    "6s": bat.get("sixes"),
                    "SR": bat.get("strikeRate")
                })

            # 🎯 Bowling
            for bowl in inning.get("bowlTeamDetails", {}).get("bowlersData", {}).values():
                bowling.append({
                    "Bowler": bowl.get("bowlName"),
                    "Overs": bowl.get("overs"),
                    "Runs": bowl.get("runs"),
                    "Wickets": bowl.get("wickets"),
                    "Economy": bowl.get("economy")
                })

            scorecard.append({
                "batting": batting,
                "bowling": bowling
            })

        return scorecard

    except Exception as e:
        print("Scorecard Error:", e)
        return []