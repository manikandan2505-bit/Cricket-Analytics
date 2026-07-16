import json
from pathlib import Path
from collections import defaultdict
import pandas as pd
import numpy as np

# ----------------------------
# Dataset location
# ----------------------------
DATASET_PATH = Path("../data/raw/t20i")
FORMAT_NAME = "T20I"

# ----------------------------
# Store batting statistics
# ----------------------------
batting_stats = defaultdict(lambda: {
    "runs": 0,
    "balls": 0,
    "fours": 0,
    "sixes": 0,
    "outs": 0
})

# ----------------------------
# Get all IPL match files
# ----------------------------
files = list(DATASET_PATH.glob("*.json"))

print(f"Found {len(files)} {FORMAT_NAME} matches")

# ----------------------------
# Process each match
# ----------------------------
for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    innings = match.get("innings", [])

    for inning in innings:

        overs = inning.get("overs", [])

        for over in overs:

            deliveries = over.get("deliveries", [])

            for ball in deliveries:

                batter = ball.get("batter")

                if batter is None:
                    continue

                runs = ball["runs"]["batter"]

                batting_stats[batter]["runs"] += runs
                batting_stats[batter]["balls"] += 1

                if runs == 4:
                    batting_stats[batter]["fours"] += 1

                elif runs == 6:
                    batting_stats[batter]["sixes"] += 1

                # Check if batter got out
                if "wickets" in ball:
                    for wicket in ball["wickets"]:
                        if wicket.get("player_out") == batter:
                            batting_stats[batter]["outs"] += 1

# ----------------------------
# Convert to DataFrame
# ----------------------------
df = pd.DataFrame.from_dict(
    batting_stats,
    orient="index"
).reset_index()

df.rename(
    columns={"index": "player"},
    inplace=True
)
df["format"] = FORMAT_NAME

# ----------------------------
# Derived metrics
# ----------------------------

# Batting Average
df["average"] = np.where(
    df["outs"] > 0,
    df["runs"] / df["outs"],
    np.nan
)

# Strike Rate
df["strike_rate"] = (
    df["runs"] / df["balls"] * 100
)

# Boundary runs
df["boundary_runs"] = (
    df["fours"] * 4 +
    df["sixes"] * 6
)

# Percentage of runs from boundaries
df["boundary_percent"] = np.where(
    df["runs"] > 0,
    (df["boundary_runs"] / df["runs"]) * 100,
    0
)

# Balls per boundary
df["balls_per_boundary"] = np.where(
    (df["fours"] + df["sixes"]) > 0,
    df["balls"] / (df["fours"] + df["sixes"]),
    np.nan
)

# ----------------------------
# Round values
# ----------------------------
numeric_columns = [
    "average",
    "strike_rate",
    "boundary_percent",
    "balls_per_boundary"
]

df[numeric_columns] = df[numeric_columns].round(2)

# ----------------------------
# Sort by total runs
# ----------------------------
df = df.sort_values(
    by="runs",
    ascending=False
)

# ----------------------------
# Show top 20 batters
# ----------------------------
print(f"\nTop 20 {FORMAT_NAME} Run Scorers\n")

print(
    df[
        [
            "player",
            "runs",
            "balls",
            "outs",
            "average",
            "strike_rate",
            "fours",
            "sixes",
            "boundary_percent"
        ]
    ].head(20)
)

# ----------------------------
# Save to CSV
# ----------------------------
export_path = Path("../exports")
export_path.mkdir(exist_ok=True)

output_file = export_path / f"batting_stats_{FORMAT_NAME.lower()}.csv"

df.to_csv(
    output_file,
    index=False
)

print(f"\nBatting statistics saved to:\n{output_file}")