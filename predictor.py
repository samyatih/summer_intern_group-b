import joblib
import pandas as pd

from pathlib import Path
from scipy.special import expit

ROOT = Path(__file__).resolve().parent

MODEL_DIR = ROOT / "models"

DATA_DIR = ROOT / "data" / "processed"

feature_cols = joblib.load(
    MODEL_DIR / "feature_columns.pkl"
)
#loading 1-6 models
models = {}

for lead in range(1, 7):

    models[lead] = joblib.load(
        MODEL_DIR /
        f"linear_enso_model_lead{lead}.pkl"
    )

#probabilities
TRANSITION_WIDTH = 0.20


def anomaly_to_probabilities(anomaly):

    p_el = expit(
        (anomaly - 0.5) /
        TRANSITION_WIDTH
    )

    p_la = expit(
        (-0.5 - anomaly) /
        TRANSITION_WIDTH
    )

    p_neutral = max(
        0,
        1 - p_el - p_la
    )

    total = p_el + p_neutral + p_la

    p_el /= total
    p_neutral /= total
    p_la /= total

    confidence = max(
        p_el,
        p_neutral,
        p_la
    )

    return (
        p_el,
        p_neutral,
        p_la,
        confidence
    )

def get_intensity(anomaly):

    value = abs(anomaly)

    if value < 0.5:
        return "Neutral"

    elif value < 1.0:
        return "Weak"

    elif value < 1.5:
        return "Moderate"

    elif value < 2.0:
        return "Strong"

    else:
        return "Very Strong"
print(models.keys())

#load master dataset
master = pd.read_csv(
    DATA_DIR / "master_enso_monthly.csv",
    parse_dates=["Date"]
)
#building latest feature vectors
def build_latest_features():

    # Keep only rows with complete observations
    latest_data = master.dropna(
        subset=[
            "nino34",
            "nino3",
            "nino4",
            "iod",
            "soi"
        ]
    ).copy()

    latest_data = latest_data.sort_values("Date")

    if len(latest_data) < 3:
        raise ValueError(
            "Need at least 3 months of observations."
        )

    latest = latest_data.iloc[-1]

    lag1 = latest_data.iloc[-2]

    lag2 = latest_data.iloc[-3]

    # 3-month rolling averages
    last3 = latest_data.tail(3)

    features = {

        "nino34": latest["nino34"],
        "nino3": latest["nino3"],
        "nino4": latest["nino4"],
        "iod": latest["iod"],
        "soi": latest["soi"],

        "nino34_lag1": lag1["nino34"],
        "nino34_lag2": lag2["nino34"],
        "nino34_lag3": latest_data.iloc[-4]["nino34"],

        "nino3_lag1": lag1["nino3"],
        "nino3_lag2": lag2["nino3"],
        "nino3_lag3": latest_data.iloc[-4]["nino3"],

        "nino4_lag1": lag1["nino4"],
        "nino4_lag2": lag2["nino4"],
        "nino4_lag3": latest_data.iloc[-4]["nino4"],

        "iod_lag1": lag1["iod"],
        "iod_lag2": lag2["iod"],
        "iod_lag3": latest_data.iloc[-4]["iod"],

        "soi_lag1": lag1["soi"],
        "soi_lag2": lag2["soi"],
        "soi_lag3": latest_data.iloc[-4]["soi"],

        "nino34_roll3": last3["nino34"].mean(),
        "nino3_roll3": last3["nino3"].mean(),
        "nino4_roll3": last3["nino4"].mean(),
        "iod_roll3": last3["iod"].mean(),
        "soi_roll3": last3["soi"].mean()

    }

    return pd.DataFrame([features])



#main eval func
def predict_enso(
    forecast_year,
    forecast_month,
    region = None
):

    latest_features = build_latest_features()

    latest_date = master.dropna(
        subset=[
            "nino34",
            "nino3",
            "nino4",
            "iod",
            "soi"
        ]
    )["Date"].max()

    latest_year = latest_date.year
    latest_month = latest_date.month

    lead = (
        (forecast_year - latest_year) * 12
        + (forecast_month - latest_month)
    )

    if lead < 1:
        raise ValueError(
            "Forecast month must be after the latest observed month."
        )

    if lead > 6:
        raise ValueError(
            f"Forecast horizon is {lead} months. "
            "This model supports only 1–6 months ahead."
        )

    model = models[lead]

    latest_features = latest_features[feature_cols]

    predicted_anomaly = model.predict(
        latest_features
    )[0]

    (
        p_el,
        p_neutral,
        p_la,
        confidence
    ) = anomaly_to_probabilities(
        predicted_anomaly
    )

    intensity = get_intensity(
        predicted_anomaly
    )

    output = pd.DataFrame({

        "Region": [region],
        
        "Year": [forecast_year],

        "Month": [forecast_month],

        "Predicted_SST_Anomaly":
            [round(predicted_anomaly, 3)],

        "El_Nino_Probability":
            [round(p_el, 3)],

        "Neutral_Probability":
            [round(p_neutral, 3)],

        "La_Nina_Probability":
            [round(p_la, 3)],

        "Forecast_Confidence":
            [round(confidence, 3)],

        "ENSO_Intensity":
            [intensity]

    })

    return output