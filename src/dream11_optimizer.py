import pandas as pd
from pulp import *

# ----------------------------------------
# Load data
# ----------------------------------------

df = pd.read_csv(
    "../exports/player_credits.csv"
)

# Remove duplicate players
df = (
    df.sort_values(
        by="overall_score",
        ascending=False
    )
    .drop_duplicates(
        subset=["player"]
    )
)

# ----------------------------------------
# Create optimization model
# ----------------------------------------

model = LpProblem(
    "Dream11_Optimizer",
    LpMaximize
)

# Decision variables
player_vars = {
    player: LpVariable(
        player,
        cat="Binary"
    )
    for player in df["player"]
}

# ----------------------------------------
# Objective function
# ----------------------------------------

model += lpSum(
    player_vars[player] *
    df.loc[
        df["player"] == player,
        "overall_score"
    ].values[0]
    for player in df["player"]
)

# ----------------------------------------
# Total players = 11
# ----------------------------------------

model += lpSum(
    player_vars[player]
    for player in df["player"]
) == 11

# ----------------------------------------
# Credit limit
# ----------------------------------------

model += lpSum(
    player_vars[player] *
    df.loc[
        df["player"] == player,
        "credits"
    ].values[0]
    for player in df["player"]
) <= 100

# ----------------------------------------
# Role constraints
# ----------------------------------------

# Exact role requirements

model += lpSum(
    player_vars[player]
    for player in df[
        df["role"] == "Utility"
    ]["player"]
) == 1

model += lpSum(
    player_vars[player]
    for player in df[
        df["role"] == "Batter"
    ]["player"]
) == 4

model += lpSum(
    player_vars[player]
    for player in df[
        df["role"] == "All-Rounder"
    ]["player"]
) == 2

model += lpSum(
    player_vars[player]
    for player in df[
        df["role"] == "Bowler"
    ]["player"]
) == 4

# ----------------------------------------
# Solve
# ----------------------------------------

model.solve()

# ----------------------------------------
# Selected team
# ----------------------------------------

selected_players = []

for player in df["player"]:

    if player_vars[player].value() == 1:

        selected_players.append(
            df[
                df["player"] == player
            ]
        )

team = pd.concat(
    selected_players
)

team = team[
    [
        "player",
        "team",
        "role",
        "credits",
        "overall_score"
    ]
]

team = team.sort_values(
    by="overall_score",
    ascending=False
)

# ----------------------------------------
# Save output
# ----------------------------------------

team.to_csv(
    "../exports/dream11_team.csv",
    index=False
)

print("\nDream XI Generated\n")

print(team)

print(
    "\nTotal Credits:",
    round(team["credits"].sum(), 1)
)

print(
    "Total Score:",
    round(team["overall_score"].sum(), 2)
)