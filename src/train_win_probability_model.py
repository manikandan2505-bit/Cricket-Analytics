import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# -----------------------------
# Load dataset
# -----------------------------

df = pd.read_csv(
    "../exports/win_probability_dataset.csv"
)

print(f"Rows loaded: {len(df):,}")

# -----------------------------
# Only second innings matter
# for win prediction
# -----------------------------

df = df[df["innings"] == 2]

# Remove invalid rows
df = df[
    (df["balls_remaining"] > 0) &
    (df["runs_required"] >= 0)
]

# -----------------------------
# Target variable
# -----------------------------

df["won"] = (
    df["batting_team"] == df["winner"]
).astype(int)

# -----------------------------
# Features
# -----------------------------

features = [
    "format",
    "batting_team",
    "bowling_team",
    "score",
    "wickets",
    "target",
    "runs_required",
    "balls_remaining",
    "current_rr",
    "required_rr"
]

X = df[features]
y = df["won"]

# -----------------------------
# Numerical features
# -----------------------------

numeric_features = [
    "score",
    "wickets",
    "target",
    "runs_required",
    "balls_remaining",
    "current_rr",
    "required_rr"
]

# -----------------------------
# Categorical features
# -----------------------------

categorical_features = [
    "format",
    "batting_team",
    "bowling_team"
]

# -----------------------------
# Preprocessing
# -----------------------------

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)

# -----------------------------
# Model
# -----------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)

# -----------------------------
# Train/Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training model...")

pipeline.fit(
    X_train,
    y_train
)

# -----------------------------
# Evaluation
# -----------------------------

predictions = pipeline.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nModel Accuracy: {accuracy:.4f}"
)

# -----------------------------
# Save model
# -----------------------------

joblib.dump(
    pipeline,
    "../exports/win_probability_model.pkl"
)

print(
    "\nModel saved successfully."
)