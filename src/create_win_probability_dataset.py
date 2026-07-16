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

            winner = info.get(
                "outcome",
                {}
            ).get(
                "winner",
                "No Result"
            )

            innings = match.get("innings", [])

            if len(innings) < 2:
                continue

            # -------------------------
            # First innings total
            # -------------------------

            first_innings_total = 0

            for over in innings[0]["overs"]:
                for delivery in over["deliveries"]:
                    first_innings_total += delivery["runs"]["total"]

            target = first_innings_total + 1

            # -------------------------
            # Process both innings
            # -------------------------

            for innings_number, inning in enumerate(
                    innings,
                    start=1):

                batting_team = inning.get(
                    "team",
                    "Unknown"
                )

                bowling_team = [
                    t for t in teams
                    if t != batting_team
                ][0]

                score = 0
                wickets = 0

                for over in inning["overs"]:

                    over_number = over["over"]

                    for ball_index, delivery in enumerate(
                            over["deliveries"],
                            start=1):

                        score += delivery["runs"]["total"]

                        if "wickets" in delivery:
                            wickets += len(
                                delivery["wickets"]
                            )

                        balls_completed = (
                            over_number * 6
                        ) + ball_index

                        balls_remaining = max(
                            120 - balls_completed,
                            0
                        )

                        overs_completed = (
                            balls_completed / 6
                        )

                        current_rr = (
                            score / overs_completed
                            if overs_completed > 0
                            else 0
                        )

                        if innings_number == 2:
                            runs_required = max(
                                target - score,
                                0
                            )

                            required_rr = (
                                runs_required /
                                (balls_remaining / 6)
                                if balls_remaining > 0
                                else 0
                            )
                        else:
                            runs_required = None
                            required_rr = None

                        records.append({
                            "match_id": match_id,
                            "format": match_format,
                            "innings": innings_number,
                            "batting_team": batting_team,
                            "bowling_team": bowling_team,
                            "over": over_number,
                            "ball": ball_index,
                            "score": score,
                            "wickets": wickets,
                            "target": target if innings_number == 2 else None,
                            "runs_required": runs_required,
                            "balls_remaining": balls_remaining,
                            "current_rr": round(
                                current_rr,
                                2
                            ),
                            "required_rr": round(
                                required_rr,
                                2
                            ) if required_rr is not None else None,
                            "winner": winner
                        })

            match_id += 1

        except Exception as e:
            print(
                f"Skipping {file}: {e}"
            )


process_folder(
    IPL_PATH,
    "IPL"
)

process_folder(
    T20I_PATH,
    "T20I"
)

df = pd.DataFrame(records)

df.to_csv(
    "../exports/win_probability_dataset.csv",
    index=False
)

print("\nDataset created successfully.")
print(
    f"Rows generated: {len(df):,}"
)