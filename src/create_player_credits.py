import pandas as pd
from pathlib import Path

# ------------------------------------
# Load master table
# ------------------------------------

df = pd.read_csv(
    "../exports/master_player_table.csv"
)

# ------------------------------------
# Normalize overall score
# ------------------------------------

max_score = df["overall_score"].max()
min_score = df["overall_score"].min()

df["credits"] = (
    6 +
    (
        (
            df["overall_score"] - min_score
        )
        /
        (
            max_score - min_score
        )
    ) * 5
)

df["credits"] = df["credits"].round(1)

# Keep Dream11 limits
df["credits"] = (
    df["credits"]
    .clip(
        lower=6,
        upper=11
    )
)

# ------------------------------------
# Save
# ------------------------------------

output_path = (
    "../exports/player_credits.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    "Credits created successfully."
)

print(
    df[
        [
            "player",
            "role",
            "overall_score",
            "credits"
        ]
    ].head(20)
)