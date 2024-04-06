from flask import Flask, render_template
import requests
from datetime import datetime, timedelta
import time
import pytz

app = Flask(__name__)

# Function to fetch previous match results, live matches, and upcoming matches
def get_scores():
    url = "https://api.football-data.org/v2/competitions/PL/matches"
    headers = {
        "X-Auth-Token": "8d4fa06b465b4742a6a4dfa28d67bbc3"  # Replace YOUR_API_KEY with your actual API key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        matches = data.get("matches", [])
        utc = pytz.utc
        ist = pytz.timezone('Asia/Kolkata')
        today = utc.localize(datetime.utcnow()).astimezone(ist)
        two_days_ago = today - timedelta(days=2)
        two_days_later = today + timedelta(days=2)
        previous_scores = []
        live_matches = []
        upcoming_matches = []
        for match in matches:
            match_time = utc.localize(datetime.fromisoformat(match['utcDate'][:-1])).astimezone(ist)
            if match_time < today and match_time >= two_days_ago:
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                result = f"{home_team} {match['score']['fullTime']['homeTeam']}-{match['score']['fullTime']['awayTeam']} {away_team}"
                previous_scores.append(result)
            elif match_time >= today and match_time < two_days_later:
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                match_info = f"{match_time.strftime('%Y-%m-%d %H:%M:%S')}: {home_team} vs {away_team}"
                upcoming_matches.append(match_info)
            elif match["status"] == "IN_PLAY":
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                score = f"{home_team} {match['score']['fullTime']['homeTeam']}-{match['score']['fullTime']['awayTeam']} {away_team}"
                live_matches.append(score)
        return previous_scores, live_matches, upcoming_matches
    else:
        print("Error fetching data:", response.status_code)
        return [], [], []

# Route to display previous match results, live matches, and upcoming matches
@app.route('/')
def display_scores():
    previous_scores, live_matches, upcoming_matches = get_scores()
    return render_template('scores.html', previous_scores=previous_scores, live_matches=live_matches, upcoming_matches=upcoming_matches)

if __name__ == "__main__":
    app.run(debug=True)
