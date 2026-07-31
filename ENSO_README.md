# ENSO Forecasting Module

## Overview

This module predicts the **Niño 3.4 Sea Surface Temperature (SST) anomaly** for **1–6 months ahead** using historical ENSO and climate index data.

The predicted SST anomaly is converted into:

- Predicted SST Anomaly (°C)
- El Niño Probability
- Neutral Probability
- La Niña Probability
- Forecast Confidence
- ENSO Intensity

This module is designed to integrate with the crop yield prediction pipeline.

---

## Data Sources

The model uses monthly observations of:

- Niño 3.4 SST Anomaly
- Niño 3 SST Anomaly
- Niño 4 SST Anomaly
- Southern Oscillation Index (SOI)
- Indian Ocean Dipole (IOD)

The processed dataset is stored in:

```
data/processed/master_enso_monthly.csv
```

---

## Feature Engineering

The model automatically constructs the following features:

Current observations:

- nino34
- nino3
- nino4
- soi
- iod

Lag features:

- lag1
- lag2
- lag3

Rolling features:

- 3-month rolling mean for all climate variables

No manual feature engineering is required during prediction.

---

## Forecast Horizons

Six independent Linear Regression models are trained.

| Model | Forecast Horizon |
|--------|------------------|
| linear_enso_model_lead1.pkl | 1 month |
| linear_enso_model_lead2.pkl | 2 months |
| linear_enso_model_lead3.pkl | 3 months |
| linear_enso_model_lead4.pkl | 4 months |
| linear_enso_model_lead5.pkl | 5 months |
| linear_enso_model_lead6.pkl | 6 months |

The predictor automatically selects the appropriate model based on the requested forecast date.

---

## Model Selection

The following models were evaluated:

- Persistence Baseline
- Linear Regression
- Random Forest
- ARIMAX

Linear Regression consistently achieved the lowest MAE and RMSE and the highest correlation across all forecast horizons and was selected as the final model.

---

## Usage

```python
from predictor import predict_enso

result = predict_enso(
    forecast_year=2026,
    forecast_month=9,
    region="Bengaluru"
)

print(result)
```

---

## Function Signature

```python
predict_enso(
    forecast_year,
    forecast_month,
    region=None
)
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| forecast_year | Target forecast year |
| forecast_month | Target forecast month |
| region | Optional region name. Included only for compatibility with the common weather interface. It does **not** affect the ENSO prediction. |

---

## Output

Example output:

| Region | Year | Month | Predicted_SST_Anomaly | El_Nino_Probability | Neutral_Probability | La_Nina_Probability | Forecast_Confidence | ENSO_Intensity |
|--------|------|-------|----------------------|--------------------|--------------------|--------------------|--------------------|---------------|
| Bengaluru | 2026 | 9 | 1.52 | 0.98 | 0.02 | 0.00 | 0.98 | Strong |

---

## Project Structure

```
summer_intern_group-b/

data/
    processed/
        master_enso_monthly.csv
        enso_features_multihorizon.csv

models/
    feature_columns.pkl
    linear_enso_model_lead1.pkl
    linear_enso_model_lead2.pkl
    linear_enso_model_lead3.pkl
    linear_enso_model_lead4.pkl
    linear_enso_model_lead5.pkl
    linear_enso_model_lead6.pkl

predictor.py
README.md
```

---

## Important Notes

- ENSO is a **global climate phenomenon**.
- The predicted ENSO values are **independent of the input region**.
- The `region` parameter is included only to maintain compatibility with the shared weather prediction interface.
- Local impacts of ENSO are handled by downstream models (e.g., crop yield prediction).

---

## Limitations

- Supports forecasts up to **6 months ahead** from the latest available observations.
- If a forecast beyond 6 months is requested, the predictor raises an error.
- The model should be retrained periodically as new monthly observations become available.

---


