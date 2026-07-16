import json
from pathlib import Path
import pandas as pd

DATASET_PATH = Path("../data/raw/t20i")
FORMAT_NAME = "T20I"

players_data = {}

files = list(DATASET_PATH.glob("*.json"))

print(f"Found {len(files)} {FORMAT_NAME} matches")

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match.get("info", {})

    teams = info.get("players", {})

    for team_name, players in teams.items():

        for player in players:

            if player not in players_data:

                players_data[player] = {
                    "player": player,
                    "team": team_name,
                    "matches": 1
                }

            else:
                players_data[player]["matches"] += 1

df = pd.DataFrame(
    list(players_data.values())
)

df = df.sort_values(
    by="matches",
    ascending=False
)

df["format"] = FORMAT_NAME

print(df.head(20))

output_file = Path(
    f"../exports/player_profiles_{FORMAT_NAME.lower()}.csv"
)

df.to_csv(
    output_file,
    index=False
)

print(f"\nSaved to {output_file}")