import pandas as pd
from pathlib import Path

exports_path = Path("../exports")

# -------------------------
# Load IPL datasets
# -------------------------
batting_ipl = pd.read_csv(exports_path / "batting_stats_ipl.csv")
batting_t20i = pd.read_csv(exports_path / "batting_stats_t20i.csv")

bowling_ipl = pd.read_csv(exports_path / "bowling_stats_ipl.csv")
bowling_t20i = pd.read_csv(exports_path / "bowling_stats_t20i.csv")

players_ipl = pd.read_csv(exports_path / "player_profiles_ipl.csv")
players_t20i = pd.read_csv(exports_path / "player_profiles_t20i.csv")

# -------------------------
# Combine formats
# -------------------------
batting = pd.concat(
    [batting_ipl, batting_t20i],
    ignore_index=True
)

bowling = pd.concat(
    [bowling_ipl, bowling_t20i],
    ignore_index=True
)

players = pd.concat(
    [players_ipl, players_t20i],
    ignore_index=True
)

# Bowling dataframe uses bowler column
bowling.rename(
    columns={"bowler": "player"},
    inplace=True
)

# -------------------------
# Merge datasets
# -------------------------
master = players.merge(
    batting,
    on=["player", "format"],
    how="left"
)

master = master.merge(
    bowling,
    on=["player", "format"],
    how="left"
)

# Replace missing values
master.fillna(0, inplace=True)

# Save
output_file = exports_path / "master_player_table.csv"

master.to_csv(
    output_file,
    index=False
)

print("\nMaster table created successfully.")
print(master.head())

print(f"\nSaved to {output_file}")