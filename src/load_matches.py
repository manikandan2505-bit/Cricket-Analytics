from pathlib import Path

ipl_path = Path("../data/raw/ipl")

files = list(ipl_path.glob("*.json"))

print(f"Total IPL matches found: {len(files)}")

print("\nFirst 5 files:")

for file in files[:5]:
    print(file.name)

import json
from pathlib import Path

sample_file = files[0]

with open(sample_file, "r", encoding="utf-8") as f:
    match = json.load(f)

print(match.keys())
print(match["info"].keys())

info = match["info"]

match_data = {
    "date": info["dates"][0],
    "team1": info["teams"][0],
    "team2": info["teams"][1],
    "venue": info.get("venue"),
    "city": info.get("city"),
}

winner = info.get("outcome", {}).get("winner")

match_data["winner"] = winner

print(match_data)