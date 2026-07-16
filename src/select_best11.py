import pandas as pd

# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("../exports/master_player_table.csv")

# -----------------------------
# Remove duplicate players
# Keep highest scoring version
# -----------------------------

df = df.sort_values(
    by="overall_score",
    ascending=False
)

df = df.drop_duplicates(
    subset=["player"]
)

# -----------------------------
# Select best batters
# -----------------------------

best_batters = (
    df[df["role"] == "Batter"]
    .sort_values(
        by="batting_score",
        ascending=False
    )
    .head(5)
)

# -----------------------------
# Select best all-rounders
# -----------------------------

best_all_rounders = (
    df[df["role"] == "All-Rounder"]
    .sort_values(
        by="overall_score",
        ascending=False
    )
    .head(2)
)

# -----------------------------
# Select best bowlers
# -----------------------------

best_bowlers = (
    df[df["role"] == "Bowler"]
    .sort_values(
        by="bowling_score",
        ascending=False
    )
    .head(4)
)

# -----------------------------
# Combine all selections
# -----------------------------

best11 = pd.concat(
    [
        best_batters,
        best_all_rounders,
        best_bowlers
    ]
)

# -----------------------------
# Sort by overall score
# -----------------------------

best11 = best11.sort_values(
    by="overall_score",
    ascending=False
)

# -----------------------------
# Save file
# -----------------------------

best11.to_csv(
    "../exports/best11.csv",
    index=False
)

# -----------------------------
# Display result
# -----------------------------

print("\nBEST PLAYING XI\n")

print(
    best11[
        [
            "player",
            "team",
            "role",
            "runs",
            "wickets",
            "overall_score"
        ]
    ]
)

print(
    "\nSaved to ../exports/best11.csv"
)