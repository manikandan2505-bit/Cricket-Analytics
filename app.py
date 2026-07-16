import streamlit as st
import pandas as pd
import joblib
import json
import gdown
from pathlib import Path

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Cricket Analytics Suite",
    page_icon="🏏",
    layout="wide"
)

# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

EXPORTS_DIR = BASE_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

MODEL_PATH = EXPORTS_DIR / "win_probability_model.pkl"

IPL_PATH = BASE_DIR / "data" / "raw" / "ipl"
T20I_PATH = BASE_DIR / "data" / "raw" / "t20i"

# ==================================================
# GOOGLE DRIVE MODEL
# ==================================================

MODEL_FILE_ID = "1SQ91EREBb-7XAcaVxvAb5WJ_y2Zzt-Io"

MODEL_URL = (
    f"https://drive.google.com/uc?id={MODEL_FILE_ID}"
)
# ==================================================
# LOAD MODEL
# ==================================================

@st.cache_resource
def load_model():

    if not MODEL_PATH.exists():

        with st.spinner(
            "Downloading machine learning model for the first time..."
        ):

            gdown.download(
                MODEL_URL,
                str(MODEL_PATH),
                quiet=False
            )

    return joblib.load(MODEL_PATH)

model = load_model()

# ==================================================
# LOAD TEAMS
# ==================================================

@st.cache_data
def load_teams():

    # ------------------------------------------
    # IPL FRANCHISES
    # ------------------------------------------

    ipl_teams = sorted([
        "Chennai Super Kings",
        "Mumbai Indians",
        "Royal Challengers Bengaluru",
        "Kolkata Knight Riders",
        "Sunrisers Hyderabad",
        "Delhi Capitals",
        "Rajasthan Royals",
        "Punjab Kings",
        "Lucknow Super Giants",
        "Gujarat Titans",
        "Deccan Chargers",
        "Pune Warriors",
        "Rising Pune Supergiant",
        "Kochi Tuskers Kerala",
        "Gujarat Lions"
    ])

    # ------------------------------------------
    # T20 INTERNATIONAL TEAMS
    # ------------------------------------------

    t20i_teams = sorted([
        "Argentina",
        "Australia",
        "Austria",
        "Bahamas",
        "Bahrain",
        "Bangladesh",
        "Belgium",
        "Belize",
        "Bermuda",
        "Bhutan",
        "Botswana",
        "Brazil",
        "Bulgaria",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Cayman Islands",
        "Chile",
        "China",
        "Cook Islands",
        "Costa Rica",
        "Croatia",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "England",
        "Estonia",
        "Eswatini",
        "Fiji",
        "Finland",
        "France",
        "Gambia",
        "Germany",
        "Ghana",
        "Gibraltar",
        "Greece",
        "Guernsey",
        "Hong Kong",
        "Hungary",
        "ICC World XI",
        "India",
        "Indonesia",
        "Iran",
        "Ireland",
        "Isle of Man",
        "Israel",
        "Italy",
        "Ivory Coast",
        "Japan",
        "Jersey",
        "Kenya",
        "Kuwait",
        "Lesotho",
        "Luxembourg",
        "Malawi",
        "Malaysia",
        "Maldives",
        "Mali",
        "Malta",
        "Mexico",
        "Mongolia",
        "Mozambique",
        "Myanmar",
        "Namibia",
        "Nepal",
        "Netherlands",
        "New Zealand",
        "Nigeria",
        "Norway",
        "Oman",
        "Pakistan",
        "Panama",
        "Papua New Guinea",
        "Philippines",
        "Portugal",
        "Qatar",
        "Romania",
        "Rwanda",
        "Samoa",
        "Saudi Arabia",
        "Scotland",
        "Serbia",
        "Seychelles",
        "Sierra Leone",
        "Singapore",
        "Slovenia",
        "South Africa",
        "South Korea",
        "Spain",
        "Sri Lanka",
        "St Helena",
        "Suriname",
        "Sweden",
        "Switzerland",
        "Tanzania",
        "Thailand",
        "Timor-Leste",
        "Turkey",
        "Turks and Caicos Islands",
        "Uganda",
        "United Arab Emirates",
        "United States of America",
        "Uzbekistan",
        "Vanuatu",
        "West Indies",
        "Zambia",
        "Zimbabwe"
    ])

    return ipl_teams, t20i_teams


ipl_teams, t20i_teams = load_teams()
# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("🏏 Cricket Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Win Predictor",
        "About Project"
    ]
)

# ==================================================
# ABOUT PAGE
# ==================================================

if page == "About Project":

    st.title("📘 About Project")

    st.markdown("""
## Features Included

- IPL Analytics Dashboard
- T20 International Analytics
- Player Intelligence Engine
- Best XI Generator
- Anchor XI Generator
- Attacking XI Generator
- Dream11 Optimizer
- Player Similarity Engine
- Win Probability Predictor
- Streamlit Deployment

## Dataset Sources

- Cricsheet IPL Dataset
- Cricsheet T20I Dataset

## Technologies Used

- Python
- Pandas
- Scikit-Learn
- Streamlit
- Power BI
- PuLP

## Project Components

- Data Engineering
- Feature Engineering
- Machine Learning
- Dashboarding
- Optimization
- Deployment
""")

# ==================================================
# WIN PREDICTOR PAGE
# ==================================================

else:

    st.title(
        "🏏 Cricket Match Win Probability Predictor"
    )

    st.markdown(
        """
Predict winning probability using machine learning models
trained on historical IPL and T20 International matches.
"""
    )

    # --------------------------------------------
    # Match Information
    # --------------------------------------------

    st.sidebar.header(
        "Match Information"
    )

    match_format = st.sidebar.selectbox(
        "Format",
        [
            "IPL",
            "T20I"
        ]
    )

    if match_format == "IPL":
        available_teams = ipl_teams
    else:
        available_teams = t20i_teams

    batting_team = st.sidebar.selectbox(
        "Batting Team",
        available_teams
    )

    bowling_options = [
        team
        for team in available_teams
        if team != batting_team
    ]

    bowling_team = st.sidebar.selectbox(
        "Bowling Team",
        bowling_options
    )

    # --------------------------------------------
    # Match Inputs
    # --------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        score = st.number_input(
            "Current Score",
            min_value=0,
            max_value=300,
            value=120
        )

        wickets = st.slider(
            "Wickets Lost",
            0,
            10,
            3
        )

    with col2:

        target = st.number_input(
            "Target",
            min_value=1,
            max_value=300,
            value=180
        )

        balls_remaining = st.slider(
            "Balls Remaining",
            1,
            120,
            42
        )

    # --------------------------------------------
    # Derived Metrics
    # --------------------------------------------

    runs_required = max(
        target - score,
        0
    )

    overs_bowled = (
        120 - balls_remaining
    ) / 6

    if overs_bowled == 0:
        current_rr = 0
    else:
        current_rr = score / overs_bowled

    if balls_remaining == 0:
        required_rr = 0
    else:
        required_rr = (
            runs_required /
            (balls_remaining / 6)
        )

    # --------------------------------------------
    # Match Situation
    # --------------------------------------------

    st.subheader(
        "📊 Current Match Situation"
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Runs Required",
        runs_required
    )

    metric2.metric(
        "Balls Remaining",
        balls_remaining
    )

    metric3.metric(
        "Current Run Rate",
        round(
            current_rr,
            2
        )
    )

    metric4.metric(
        "Required Run Rate",
        round(
            required_rr,
            2
        )
    )

    # --------------------------------------------
    # Prediction
    # --------------------------------------------

    if st.button(
        "Predict Win Probability"
    ):

        input_df = pd.DataFrame([{
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
        }])

        prediction = model.predict_proba(
            input_df
        )[0]

        batting_probability = (
            prediction[1] * 100
        )

        bowling_probability = (
            prediction[0] * 100
        )

        st.divider()

        st.header(
            "📈 Match Prediction"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                batting_team
            )

            st.metric(
                "Winning Probability",
                f"{batting_probability:.2f}%"
            )

            st.progress(
                batting_probability / 100
            )

        with col2:

            st.subheader(
                bowling_team
            )

            st.metric(
                "Winning Probability",
                f"{bowling_probability:.2f}%"
            )

            st.progress(
                bowling_probability / 100
            )

        # ----------------------------------------
        # Momentum Meter
        # ----------------------------------------

        if batting_probability >= 80:
            momentum = "🔥 Dominating"

        elif batting_probability >= 65:
            momentum = "📈 Positive Momentum"

        elif batting_probability >= 50:
            momentum = "⚖ Balanced"

        elif batting_probability >= 35:
            momentum = "📉 Under Pressure"

        else:
            momentum = "🚨 Collapse Risk"

        st.subheader(
            f"Momentum: {momentum}"
        )

        # ----------------------------------------
        # Match Verdict
        # ----------------------------------------

        if batting_probability > bowling_probability:

            st.success(
                f"{batting_team} are favourites to win."
            )

        else:

            st.error(
                f"{bowling_team} are favourites to win."
            )