import json
from pathlib import Path
from collections import defaultdict
import pandas as pd
import numpy as np

# ==========================================
# Dataset Location
# ==========================================
DATASET_PATH = Path("../data/raw/t20i")
FORMAT_NAME = "T20I"

# ==========================================
# Bowling Statistics Storage
# ==========================================
bowling_stats = defaultdict(lambda: {
    "balls": 0,
    "runs_conceded": 0,
    "wickets": 0,
    "dot_balls": 0,
    "fours_conceded": 0,
    "sixes_conceded": 0
})

# ==========================================
# Get Match Files
# ==========================================
files = list(DATASET_PATH.glob("*.json"))

print(f"Found {len(files)} {FORMAT_NAME} matches")

# ==========================================
# Process Matches
# ==========================================
for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    innings = match.get("innings", [])

    for inning in innings:

        overs = inning.get("overs", [])

        for over in overs:

            deliveries = over.get("deliveries", [])

            for ball in deliveries:

                bowler = ball.get("bowler")

                if not bowler:
                    continue

                total_runs = ball["runs"]["total"]
                batter_runs = ball["runs"]["batter"]

                # Ball bowled
                bowling_stats[bowler]["balls"] += 1

                # Runs conceded
                bowling_stats[bowler]["runs_conceded"] += total_runs

                # Dot ball
                if total_runs == 0:
                    bowling_stats[bowler]["dot_balls"] += 1

                # Boundary conceded
                if batter_runs == 4:
                    bowling_stats[bowler]["fours_conceded"] += 1

                elif batter_runs == 6:
                    bowling_stats[bowler]["sixes_conceded"] += 1

                # Wickets
                if "wickets" in ball:

                    for wicket in ball["wickets"]:

                        dismissal_type = wicket.get("kind")

                        # Bowler does not get credit for these
                        if dismissal_type not in [
                            "run out",
                            "retired hurt",
                            "retired out",
                            "obstructing the field"
                        ]:
                            bowling_stats[bowler]["wickets"] += 1

# ==========================================
# Convert To DataFrame
# ==========================================
df = pd.DataFrame.from_dict(
    bowling_stats,
    orient="index"
).reset_index()

df.rename(
    columns={"index": "bowler"},
    inplace=True
)
df["format"] = FORMAT_NAME

# ==========================================
# Derived Metrics
# ==========================================

# Overs Bowled
df["overs"] = (df["balls"] / 6).round(1)

# Economy Rate
df["economy"] = np.where(
    df["overs"] > 0,
    df["runs_conceded"] / df["overs"],
    np.nan
)

# Bowling Average
df["bowling_average"] = np.where(
    df["wickets"] > 0,
    df["runs_conceded"] / df["wickets"],
    np.nan
)

# Bowling Strike Rate
df["bowling_strike_rate"] = np.where(
    df["wickets"] > 0,
    df["balls"] / df["wickets"],
    np.nan
)

# Dot Ball Percentage
df["dot_ball_percent"] = (
    df["dot_balls"] / df["balls"] * 100
)

# Boundary Runs Conceded
df["boundary_runs_conceded"] = (
    df["fours_conceded"] * 4 +
    df["sixes_conceded"] * 6
)

# Boundary Percentage Conceded
df["boundary_percent_conceded"] = np.where(
    df["runs_conceded"] > 0,
    (
        df["boundary_runs_conceded"] /
        df["runs_conceded"]
    ) * 100,
    0
)

# Balls Per Boundary Conceded
df["balls_per_boundary"] = np.where(
    (df["fours_conceded"] + df["sixes_conceded"]) > 0,
    df["balls"] /
    (df["fours_conceded"] + df["sixes_conceded"]),
    np.nan
)

# ==========================================
# Round Metrics
# ==========================================
numeric_columns = [
    "economy",
    "bowling_average",
    "bowling_strike_rate",
    "dot_ball_percent",
    "boundary_percent_conceded",
    "balls_per_boundary"
]

df[numeric_columns] = df[numeric_columns].round(2)

# ==========================================
# Sort By Wickets
# ==========================================
df = df.sort_values(
    by="wickets",
    ascending=False
)

# ==========================================
# Display Top Bowlers
# ==========================================
print(f"\nTop 20 {FORMAT_NAME} Wicket Takers\n")

print(
    df[
        [
            "bowler",
            "wickets",
            "runs_conceded",
            "overs",
            "economy",
            "bowling_average",
            "bowling_strike_rate",
            "dot_ball_percent"
        ]
    ].head(20)
)

# ==========================================
# Export CSV
# ==========================================
export_path = Path("../exports")
export_path.mkdir(exist_ok=True)

output_file = export_path / f"bowling_stats_{FORMAT_NAME.lower()}.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nBowling statistics saved successfully.")
print(f"File location: {output_file}")