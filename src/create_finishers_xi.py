import pandas as pd

df = pd.read_csv("../exports/master_player_table.csv")

# Fill missing values
df["strike_rate"] = df["strike_rate"].fillna(0)
df["boundary_percent"] = df["boundary_percent"].fillna(0)
df["balls_per_boundary_x"] = (
    df["balls_per_boundary_x"]
    .fillna(999)
)

# Remove players with very few runs
df = df[df["runs"] >= 500]

# Lower balls per boundary is better
boundary_speed_score = (
    20 - df["balls_per_boundary_x"]
).clip(lower=0)

# Finisher score
df["finisher_score"] = (
    df["strike_rate"] * 0.5 +
    df["boundary_percent"] * 0.3 +
    boundary_speed_score * 0.2
)

finishers = (
    df.sort_values(
        by="finisher_score",
        ascending=False
    )
    .drop_duplicates(subset=["player"])
    .head(11)
)

finishers.to_csv(
    "../exports/finishers_xi.csv",
    index=False
)

print("\nBest Finishers XI\n")

print(
    finishers[
        [
            "player",
            "team",
            "runs",
            "strike_rate",
            "boundary_percent",
            "balls_per_boundary_x",
            "finisher_score"
        ]
    ]
)

print("\nSaved to ../exports/finishers_xi.csv")