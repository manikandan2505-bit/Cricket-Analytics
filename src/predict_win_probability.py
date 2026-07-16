import joblib
import pandas as pd

# -----------------------------
# Load model
# -----------------------------

model = joblib.load(
    "../exports/win_probability_model.pkl"
)

# -----------------------------
# User Input
# -----------------------------

match_format = input(
    "Format (IPL/T20I): "
)

batting_team = input(
    "Batting Team: "
)

bowling_team = input(
    "Bowling Team: "
)

score = int(
    input(
        "Current Score: "
    )
)

wickets = int(
    input(
        "Wickets Lost: "
    )
)

target = int(
    input(
        "Target: "
    )
)

balls_remaining = int(
    input(
        "Balls Remaining: "
    )
)

# -----------------------------
# Derived Features
# -----------------------------

runs_required = target - score

current_rr = (
    score /
    ((120 - balls_remaining) / 6)
)

required_rr = (
    runs_required /
    (balls_remaining / 6)
)

# -----------------------------
# Create Input DataFrame
# -----------------------------

sample = pd.DataFrame(
    [{
        "format": match_format,
        "batting_team": batting_team,
        "bowling_team": bowling_team,
        "score": score,
        "wickets": wickets,
        "target": target,
        "runs_required": runs_required,
        "balls_remaining": balls_remaining,
        "current_rr": round(
            current_rr,
            2
        ),
        "required_rr": round(
            required_rr,
            2
        )
    }]
)

# -----------------------------
# Prediction
# -----------------------------

probability = model.predict_proba(
    sample
)[0]

lose_probability = probability[0] * 100
win_probability = probability[1] * 100

print("\n==============================")
print("WIN PROBABILITY")
print("==============================")

print(
    f"{batting_team}: "
    f"{win_probability:.2f}%"
)

print(
    f"{bowling_team}: "
    f"{lose_probability:.2f}%"
)