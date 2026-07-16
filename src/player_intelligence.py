import pandas as pd
from pathlib import Path

df = pd.read_csv(
    "../exports/master_player_table.csv"
)

strengths = []
weaknesses = []

for _, row in df.iterrows():

    player_strengths = []
    player_weaknesses = []

    # --------------------
    # Batting Intelligence
    # --------------------
    if row["runs"] > 3000:
        player_strengths.append("Experienced Batter")

    if row["strike_rate"] >= 145:
        player_strengths.append("Aggressive Batter")

    if row["average"] >= 35:
        player_strengths.append("Consistent Batter")

    if row["boundary_percent"] >= 55:
        player_strengths.append("Boundary Hitter")

    if row["strike_rate"] < 120 and row["runs"] > 500:
        player_weaknesses.append("Slow Scorer")

    # --------------------
    # Bowling Intelligence
    # --------------------
    if row["wickets"] >= 100:
        player_strengths.append("Wicket Taking Bowler")

    if row["economy"] > 0 and row["economy"] < 7:
        player_strengths.append("Economical Bowler")

    if row["dot_ball_percent"] >= 40:
        player_strengths.append("Creates Pressure")

    if row["economy"] > 9:
        player_weaknesses.append("Expensive Bowler")

    # Handle empty values
    if len(player_strengths) == 0:
        player_strengths.append("Developing Player")

    if len(player_weaknesses) == 0:
        player_weaknesses.append("No Major Weakness Detected")

    strengths.append(", ".join(player_strengths))
    weaknesses.append(", ".join(player_weaknesses))

df["strengths"] = strengths
df["weaknesses"] = weaknesses

output_file = "../exports/player_intelligence.csv"

df.to_csv(
    output_file,
    index=False
)

print(
    df[
        [
            "player",
            "format",
            "strengths",
            "weaknesses"
        ]
    ].head(20)
)

print(f"\nSaved to {output_file}")