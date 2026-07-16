import os
import json
import pandas as pd

IPL_PATH = "../data/raw/ipl"
T20I_PATH = "../data/raw/t20i"

records = []
match_id = 1


def process_folder(folder_path, match_format):
    global match_id

    files = os.listdir(folder_path)

    for file in files:
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(folder_path, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                match = json.load(f)

            info = match["info"]

            teams = info.get("teams", [])

            if len(teams) != 2:
                continue

            team1 = teams[0]
            team2 = teams[1]

            winner = info.get("outcome", {}).get("winner", "No Result")

            innings = match.get("innings", [])

            if len(innings) < 2:
                continue

            first_score = 0
            second_score = 0

            # First innings score
            for over in innings[0]["overs"]:
                for delivery in over["deliveries"]:
                    first_score += delivery["runs"]["total"]

            # Second innings score
            for over in innings[1]["overs"]:
                for delivery in over["deliveries"]:
                    second_score += delivery["runs"]["total"]

            records.append({
                "match_id": match_id,
                "team1": team1,
                "team2": team2,
                "first_innings_score": first_score,
                "second_innings_score": second_score,
                "winner": winner,
                "format": match_format
            })

            match_id += 1

        except Exception as e:
            print(f"Skipping {file}: {e}")


process_folder(IPL_PATH, "IPL")
process_folder(T20I_PATH, "T20I")

df = pd.DataFrame(records)

output_path = "../exports/match_summary.csv"

df.to_csv(output_path, index=False)

print("===================================")
print("Match Summary Created Successfully")
print("===================================")
print(f"Total Matches : {len(df)}")
print(f"Saved to : {output_path}")