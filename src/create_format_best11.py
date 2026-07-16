import pandas as pd

# Load master table
df = pd.read_csv("../exports/master_player_table.csv")

# Remove duplicates within same format
df = df.sort_values(
    by="overall_score",
    ascending=False
)

df = df.drop_duplicates(
    subset=["player", "format"]
)

formats = ["IPL", "T20I"]

for cricket_format in formats:

    print(f"\nCreating Best XI for {cricket_format}")

    format_df = df[
        df["format"] == cricket_format
    ]

    # Best Batters
    batters = (
        format_df[
            format_df["role"] == "Batter"
        ]
        .sort_values(
            by="batting_score",
            ascending=False
        )
        .head(5)
    )

    # Best All-rounders
    all_rounders = (
        format_df[
            format_df["role"] == "All-Rounder"
        ]
        .sort_values(
            by="overall_score",
            ascending=False
        )
        .head(2)
    )

    # Best Bowlers
    bowlers = (
        format_df[
            format_df["role"] == "Bowler"
        ]
        .sort_values(
            by="bowling_score",
            ascending=False
        )
        .head(4)
    )

    best11 = pd.concat(
        [
            batters,
            all_rounders,
            bowlers
        ]
    )

    best11 = best11.sort_values(
        by="overall_score",
        ascending=False
    )

    output_file = (
        f"../exports/best11_{cricket_format.lower()}.csv"
    )

    best11.to_csv(
        output_file,
        index=False
    )

    print(
        best11[
            [
                "player",
                "role",
                "overall_score"
            ]
        ]
    )

    print(
        f"\nSaved to {output_file}"
    )