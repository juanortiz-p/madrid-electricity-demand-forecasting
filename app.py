import json
import subprocess
import sys

import pandas as pd
import streamlit as st

from datetime import date, datetime, time, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
INPUT_DIR = PROJECT_ROOT / "data" / "input"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"

NOTEBOOKS = [
    "01_get_api_redes.ipynb",
    "02_get_api_meteo.ipynb",
    "03_holidays.ipynb",
    "04_unify_forecast_dataset.ipynb",
    "05_forecast.ipynb",
]

PERIODS_PATH = INPUT_DIR / "periods.json"
METRICS_PATH = OUTPUT_DIR / "metrics.json"
FORECAST_PLOT_PATH = OUTPUT_DIR / "forecast_plot.png"
FEATURE_IMPORTANCE_PATH = OUTPUT_DIR / "feature_importance.csv"


st.set_page_config(
    page_title="Electricity Demand Forecasting",
    page_icon="⚡",
    layout="wide",
)


st.title("⚡ Electricity Demand Forecasting")

st.write(
    """
    This project forecasts daily electricity demand using:

    - Electricity-demand data from REData
    - Weather data from AEMET
    - Spanish national holidays
    - Calendar and historical demand features
    - A LightGBM regression model
    """
)

st.divider()

def create_periods(start_date, end_date):
    periods = []
    current_start = start_date

    while current_start <= end_date:
        if current_start.month <= 6:
            current_end = date(
                current_start.year,
                6,
                30,
            )
        else:
            current_end = date(
                current_start.year,
                12,
                31,
            )
        current_end = min(current_end, end_date)

        start_text = (
            datetime.combine(
                current_start,
                time.min,
            ).strftime("%Y-%m-%dT%H:%M:%SUTC")
        )
        end_text = (
            datetime.combine(
                current_end,
                time(23, 59, 59),
            ).strftime("%Y-%m-%dT%H:%M:%SUTC")
        )
        periods.append((start_text, end_text))
        current_start = current_end + timedelta(days=1)

    return periods
def save_periods(periods):
    PERIODS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    config = {
        "periods": periods,
    }

    with open(
        PERIODS_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            config,
            file,
            indent=4,
        )

def run_notebook(notebook_name):
    notebook_path = NOTEBOOKS_DIR / notebook_name

    command = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        notebook_path.name,
        "--ExecutePreprocessor.timeout=600",
    ]

    result = subprocess.run(
        command,
        cwd=NOTEBOOKS_DIR,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

st.header("Run pipeline")

st.write(
    """
    Select the historical period used to download electricity-demand
    and weather data.
    """
)

selected_dates = st.date_input(
    "Data period",
    value=(
        date(2025, 1, 1),
        date(2026, 6, 30),
    ),
    min_value=date(2020, 1, 1),
    max_value=date.today(),
    format="DD/MM/YYYY",
)

st.info(
    "The default period, from January 2025 to June 2026, "
    "takes approximately 2 minutes to execute."
)

valid_date_range = (
    isinstance(selected_dates, tuple)
    and len(selected_dates) == 2
)

if valid_date_range:
    start_date, end_date = selected_dates

    periods = create_periods(
        start_date=start_date,
        end_date=end_date,
    )

    with st.expander("View API request periods"):
        for period_start, period_end in periods:
            st.write(
                f"`{period_start}` → `{period_end}`"
            )
else:
    st.warning("Select both a start date and an end date.")
    periods = []


col1, col2 = st.columns(2)

with col1:
    run_pipeline = st.button(
        "▶ Run complete pipeline",
        type="primary",
        disabled=not valid_date_range,
        use_container_width=True,
    )

with col2:
    reload_outputs = st.button(
        "↻ Reload outputs",
        use_container_width=True,
    )

if reload_outputs:
    st.rerun()

if run_pipeline:

    save_periods(periods)

    progress_bar = st.progress(0)
    status = st.empty()

    try:
        for index, notebook in enumerate(NOTEBOOKS):

            status.write(f"Running `{notebook}`...")

            run_notebook(notebook)

            progress_bar.progress(
                (index + 1) / len(NOTEBOOKS)
            )

        status.success(
            "Pipeline completed successfully. Reloading outputs..."
        )

        st.session_state["pipeline_completed"] = True

        st.rerun()

    except Exception as error:
        status.error(
            "The pipeline could not be completed."
        )

        with st.expander("Show error"):
            st.code(str(error))


st.divider()
st.header("Model results")

if METRICS_PATH.exists():
    with open(METRICS_PATH, encoding="utf-8") as file:
        metrics = json.load(file)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Baseline MAE",
        f"{metrics['baseline_mae']:,.2f}",
    )

    col2.metric(
        "Baseline MAPE",
        f"{metrics['baseline_mape']:.2%}",
    )

    col3.metric(
        "LightGBM MAE",
        f"{metrics['model_mae']:,.2f}",
    )

    col4.metric(
        "LightGBM MAPE",
        f"{metrics['model_mape']:.2%}",
    )
else:
    st.info(
        "Run the pipeline to generate the model metrics."
    )


st.subheader("Forecast")

if FORECAST_PLOT_PATH.exists():
    st.image(
        str(FORECAST_PLOT_PATH),
        use_container_width=True,
    )
else:
    st.info(
        "The forecast plot has not been generated yet."
    )


st.subheader("Feature importance")

if FEATURE_IMPORTANCE_PATH.exists():
    feature_importance = pd.read_csv(
        FEATURE_IMPORTANCE_PATH
    )

    st.bar_chart(
        feature_importance.set_index("feature")[
            "importance"
        ]
    )

    with st.expander("View feature importance data"):
        st.dataframe(
            feature_importance,
            use_container_width=True,
            hide_index=True,
        )
else:
    st.info(
        "Feature importance has not been generated yet."
    )