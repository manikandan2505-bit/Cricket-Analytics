import pandas as pd

df = pd.read_csv("../exports/master_player_table.csv")

# Remove players with very small sample size
df = df[df["runs"] >= 1000]

# Fill missing values
df["average"] = df["average"].fillna(0)
df["strike_rate"] = df["strike_rate"].fillna(0)

# Normalize runs because runs are much larger numbers
max_runs = df["runs"].max()

df["normalized_runs"] = (
    df["runs"] / max_runs
) * 100

# Anchor Score
df["anchor_score"] = (
    df["average"] * 0.5 +
    df["normalized_runs"] * 0.3 +
    df["strike_rate"] * 0.2
)

anchors = (
    df.sort_values(
        by="anchor_score",
        ascending=False
    )
    .drop_duplicates(
        subset=["player"]
    )
    .head(11)
)

anchors.to_csv(
    "../exports/anchor_xi.csv",
    index=False
)

print("\nBest Anchor XI\n")

print(
    anchors[
        [
            "player",
            "team",
            "runs",
            "average",
            "strike_rate",
            "anchor_score"
        ]
    ]
)

print(
    "\nSaved to ../exports/anchor_xi.csv"
)