import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("../exports/master_player_table.csv")

# Remove duplicate player entries
df = df.sort_values(
    by="overall_score",
    ascending

df = df.drop_duplicates(
    subset=["player"]
)

features = [
    "average",
    "strike_rate",
    "boundary_percent",
    "wickets",
    "economy",
    "dot_ball_percent"
]

df[features] = df[features].fillna(0)

# Scale features
scaler = StandardScaler()
scaled = scaler.fit_transform(df[features])

# Similarity matrix
similarity_matrix = cosine_similarity(scaled)

rows = []

for i, player1 in enumerate(df["player"]):

    similarities = similarity_matrix[i]

    for j, player2 in enumerate(df["player"]):

        if player1 == player2:
            continue

        rows.append({
            "selected_player": player1,
            "similar_player": player2,
            "similarity_score": similarities[j]
        })

similarity_df = pd.DataFrame(rows)

# Keep top 5 similar players for each player
similarity_df = (
    similarity_df
    .sort_values(
        ["selected_player", "similarity_score"],
        ascending=[True, False]
    )
    .groupby("selected_player")
    .head(5)
)

similarity_df.to_csv(
    "../exports/player_similarity.csv",
    index=False
)

print("player_similarity.csv created successfully")