# ⚡ Madrid Electricity Demand Forecasting

> End-to-end Machine Learning project for forecasting **hourly electricity demand in the Community of Madrid** using historical demand, weather data and calendar features.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![LightGBM](https://img.shields.io/badge/LightGBM-Gradient%20Boosting-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

# 📌 Overview

Electricity demand forecasting is one of the most important problems in the energy industry.

Utilities, grid operators and energy retailers need accurate demand forecasts to:

- reduce operational costs
- optimize energy purchases
- improve grid stability
- anticipate demand peaks
- support decision making

This project predicts the **hourly electricity demand of the Community of Madrid for the next 24 hours** using historical electricity demand published by **Red Eléctrica (REData API)** and weather observations from **AEMET OpenData**. REData provides a public REST API for accessing electricity system data, while AEMET OpenData offers a REST API for meteorological observations and forecasts. :contentReference[oaicite:0]{index=0}

---

# 🎯 Objective

Build an end-to-end forecasting system capable of predicting:

> **Electricity demand (MW) for every hour of the next day in Madrid.**

The system should automatically:

- download new data
- generate features
- train the model
- evaluate performance
- produce daily forecasts
- expose predictions through an API

---

# 🗂 Dataset

## Electricity Demand

Source:

- REData API (Red Eléctrica)

Variables:

- timestamp
- electricity demand (MW)

Granularity:

- hourly

Region:

- Community of Madrid

---

## Weather

Source:

- AEMET OpenData

Variables:

- temperature
- humidity
- precipitation
- wind speed
- atmospheric pressure

Weather has a strong influence on electricity demand because heating and air conditioning significantly increase consumption during extreme temperatures. AEMET OpenData exposes these observations and forecasts through a free REST API (API key required). :contentReference[oaicite:1]{index=1}

---

## Calendar Features

Generated locally.

Examples:

- hour
- weekday
- month
- weekend
- holiday
- day before holiday
- season

---

# 🧠 Machine Learning Problem

Type:

Regression

Target variable:

```text
electricity_demand_mw
```

Forecast horizon:

```text
24 hours ahead
```

Frequency:

```text
Hourly
```

---

# 📊 Feature Engineering

## Temporal Features

- hour
- weekday
- month
- week of year
- weekend
- holidays

---

## Cyclical Encoding

- hour_sin
- hour_cos
- month_sin
- month_cos

---

## Lag Features

- demand_lag_1
- demand_lag_2
- demand_lag_24
- demand_lag_48
- demand_lag_168

---

## Rolling Statistics

- rolling_mean_24h
- rolling_mean_7d
- rolling_std_24h
- rolling_max_24h

---

## Weather Features

- temperature
- min_temperature
- max_temperature
- humidity
- rainfall
- wind_speed

---

# 🤖 Models

The project compares several forecasting approaches.

## Baseline

Yesterday's same hour

```python
prediction = demand[t-24]
```

---

## Baseline

Same hour last week

```python
prediction = demand[t-168]
```

---

## Statistical Model

- SARIMA

---

## Machine Learning

- LightGBM ⭐

Future versions:

- XGBoost
- CatBoost
- LSTM
- Temporal Fusion Transformer

---

# 📈 Evaluation

The dataset is split chronologically.

```text
Train      2021-2023
Validation 2024
Test       2025
```

No random split is performed.

Metrics:

- MAE
- RMSE
- MAPE

Additional analysis:

- error by hour
- weekends vs weekdays
- holidays
- extreme temperatures

---

# 📦 Project Structure

```text
madrid-electricity-demand-forecasting/

│

├── data/

│   ├── raw/

│   ├── processed/

│   └── external/

│

├── notebooks/

│

├── src/

│   ├── data/

│   ├── features/

│   ├── models/

│   ├── evaluation/

│   └── visualization/

│

├── api/

│

├── dashboard/

│

├── models/

│

├── tests/

│

├── Dockerfile

├── requirements.txt

└── README.md
```

---

# 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Scikit-Learn
- LightGBM
- FastAPI
- Streamlit
- Docker
- GitHub Actions
- VS Code

Future:

- MLflow
- DVC
- Prefect

---

# 🚀 Roadmap

## Version 1

- [ ] Download REData data
- [ ] Download AEMET weather
- [ ] Clean datasets
- [ ] Merge datasets
- [ ] Feature engineering
- [ ] Baseline models
- [ ] LightGBM model
- [ ] Model evaluation

---

## Version 2

- [ ] FastAPI inference API
- [ ] Streamlit dashboard
- [ ] Forecast visualization
- [ ] Feature importance
- [ ] SHAP explainability

---

## Version 3

- [ ] Automatic daily retraining
- [ ] Docker deployment
- [ ] CI/CD
- [ ] Model monitoring
- [ ] Data validation

---

# 📊 Example Output

| Hour | Predicted Demand (MW) |
|-------|----------------------:|
| 00:00 | 4,850 |
| 01:00 | 4,620 |
| 02:00 | 4,480 |
| ... | ... |
| 19:00 | 7,320 |
| 20:00 | 7,510 |
| 21:00 | 7,260 |

---

# 📚 Data Sources

- **REData API (Red Eléctrica)** – Official public API providing electricity system data through REST endpoints. :contentReference[oaicite:2]{index=2}
- **AEMET OpenData** – Official REST API for meteorological observations and forecasts (free with API key). :contentReference[oaicite:3]{index=3}

---

# 📄 License

MIT License
