from predictor import predict_enso

result = predict_enso(
    forecast_year=2026,
    forecast_month=7,
    region="Bengaluru"
)

print(result.to_string(index=False))