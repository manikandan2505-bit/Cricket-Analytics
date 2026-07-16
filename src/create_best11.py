import pandas as pd
import numpy as np

# ----------------------------
# Load data
# ----------------------------

df = pd.read_csv("../exports/master_player_table.csv")

# ----------------------------
# Fill missing values
# ----------------------------

numeric_columns = [
    "runs",
    "wickets",
    "average",
    "strike_rate",
    "economy",
    "boundary_percent",
    "dot_ball_percent"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# ----------------------------
# Batting Score
# ----------------------------

df["batting_score"] = (
    df["average"] * 0.40 +
    df["strike_rate"] * 0.40 +
    df["boundary_percent"] * 0.20
)

# ----------------------------
# Bowling Score
# ----------------------------

economy_score = (
    10 - df["economy"]
).clip(lower=0)

df["bowling_score"] = (
    economy_score * 5 +
    df["wickets"] * 0.40 +
    df["dot_ball_percent"] * 0.20
)

# ----------------------------
# Overall Score
# ----------------------------

df["overall_score"] = (
    df["batting_score"] +
    df["bowling_score"]
)

# ----------------------------
# Save updated dataset
# ----------------------------

df.to_csv(
    "../exports/master_player_table.csv",
    index=False
)

print("\nScores generated successfully.\n")

print(
    df[
        [
            "player",
            "role",
            "batting_score",
            "bowling_score",
            "overall_score"
        ]
    ].head(20)
)