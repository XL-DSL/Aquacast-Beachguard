import pandas as pd
import streamlit as st

from utils.live_forecast import load_live_latest
from utils.styles import apply_styles
from utils.ui import render_footer
from utils.validation import (
    APP_VERSION,
    validate_prediction_row,
    validate_saved_csv,
)


st.set_page_config(
    page_title="Model & Data | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("Model & Data")

st.caption(
    "Model design, data sources, thresholds, "
    "performance, and current data status."
)


# ==========================================================
# DATA STATUS
# ==========================================================

st.subheader("Data Status")


try:
    current = load_live_latest()

    current_result = validate_prediction_row(
        current
    )

    live_status = "Available"

except Exception:
    current = None

    current_result = {
        "valid": False,
        "warnings": [],
        "errors": [
            "Live prediction unavailable."
        ],
        "stale": False,
    }

    live_status = "Unavailable"


saved_df, saved_status = validate_saved_csv()


status_col1, status_col2, status_col3, status_col4 = st.columns(
    4
)


with status_col1:
    st.metric(
        "Live Forecast",
        live_status,
    )


with status_col2:
    st.metric(
        "Current Validation",
        (
            "Pass"
            if current_result["valid"]
            else "Fail"
        ),
    )


with status_col3:
    st.metric(
        "Saved Valid Rows",
        saved_status["valid_rows"],
    )


with status_col4:
    st.metric(
        "App Version",
        APP_VERSION,
    )


status_table = pd.DataFrame(
    [
        {
            "Check": "Saved CSV load",
            "Status": (
                "Pass"
                if saved_status["loaded"]
                else "Fail"
            ),
        },
        {
            "Check": "Required columns",
            "Status": (
                "Pass"
                if not saved_status["missing_columns"]
                else "Fail"
            ),
        },
        {
            "Check": "Duplicate records",
            "Status": (
                "Pass"
                if saved_status["duplicate_count"] == 0
                else "Fail"
            ),
        },
        {
            "Check": "Invalid rows",
            "Status": saved_status["invalid_rows"],
        },
        {
            "Check": "Saved forecast stale",
            "Status": (
                "Yes"
                if saved_status["stale"]
                else "No"
            ),
        },
    ]
)


st.dataframe(
    status_table,
    hide_index=True,
    use_container_width=True,
)


if current_result["errors"]:
    with st.expander(
        "Current validation details"
    ):
        for error in current_result["errors"]:
            st.write(
                f"• {error}"
            )


if current_result["warnings"]:
    with st.expander(
        "Current validation warnings"
    ):
        for warning in current_result["warnings"]:
            st.write(
                f"• {warning}"
            )


# ==========================================================
# WHAT AQUACAST PREDICTS
# ==========================================================

st.subheader("What AquaCast Predicts")

st.write(
    """
AquaCast estimates the probability that
**E. coli** or **Enterococcus** will exceed an
elevated-risk concentration threshold at
**Parkside Aquatic Park, San Mateo**.

The system performs classification rather than
predicting an exact bacterial concentration.

Direct bacterial concentrations require
laboratory measurement.
"""
)


# ==========================================================
# DATA SOURCES
# ==========================================================

st.subheader("Data Sources")

st.markdown(
    """
- **California Water Boards / California Open Data**  
  Historical fecal-indicator bacteria monitoring observations.

- **NOAA / NCEI**  
  Historical precipitation and temperature observations used
  during model development.

- **Open-Meteo**  
  Recent and forecast weather used by the live forecast layer.

Tide and sanitary-sewer-overflow variables were considered
during earlier development but are not final V2 model inputs.
"""
)


# ==========================================================
# RISK THRESHOLDS
# ==========================================================

st.subheader("Risk Thresholds")


thresholds = pd.DataFrame(
    [
        {
            "Bacterium": "E. coli",
            "Safe": "<10%",
            "Caution": "10% to <50%",
            "Unsafe": "≥50%",
            "Concentration Threshold": "235 MPN/100 mL",
        },
        {
            "Bacterium": "Enterococcus",
            "Safe": "<40%",
            "Caution": "40% to <85%",
            "Unsafe": "≥85%",
            "Concentration Threshold": "130 MPN/100 mL",
        },
    ]
)


st.dataframe(
    thresholds,
    hide_index=True,
    use_container_width=True,
)


st.info(
    "The Safe, Caution, and Unsafe probability boundaries "
    "are AquaCast display thresholds. "
    "They are separate from the underlying bacterial "
    "concentration thresholds."
)


# ==========================================================
# FEATURE GROUPS
# ==========================================================

st.subheader("Feature Groups")


features = pd.DataFrame(
    [
        {
            "Feature Group": "Short-term rainfall",
            "Examples": (
                "rain_1day, rain_3day_sum, "
                "rain lags"
            ),
        },
        {
            "Feature Group": "Rainfall pattern",
            "Examples": (
                "rain ratios, rolling rainfall, "
                "rain intensity"
            ),
        },
        {
            "Feature Group": "Temperature",
            "Examples": (
                "3-day, 7-day, and 14-day "
                "temperature averages"
            ),
        },
        {
            "Feature Group": "Dry period / first flush",
            "Examples": (
                "adp_days, first_flush_index"
            ),
        },
        {
            "Feature Group": "Seasonal / interaction",
            "Examples": (
                "wet season and "
                "rain-temperature interactions"
            ),
        },
        {
            "Feature Group": "Previous bacteria history",
            "Examples": (
                "previous laboratory results and "
                "prior exceedance indicators"
            ),
        },
    ]
)


st.dataframe(
    features,
    hide_index=True,
    use_container_width=True,
)


# ==========================================================
# DOCUMENTED MODEL PERFORMANCE
# ==========================================================

st.subheader("Documented Final V2 Performance")


performance = pd.DataFrame(
    [
        {
            "Bacterium": "E. coli",
            "Model": (
                "Logistic Regression / "
                "expanded no-tides"
            ),
            "Recall": 0.950,
            "Precision": 0.533,
            "F1": 0.683,
            "PR-AUC": 0.767,
        },
        {
            "Bacterium": "Enterococcus",
            "Model": (
                "Logistic Regression / "
                "base no-SSO"
            ),
            "Recall": 0.657,
            "Precision": 0.657,
            "F1": 0.657,
            "PR-AUC": 0.691,
        },
    ]
)


st.dataframe(
    performance,
    hide_index=True,
    use_container_width=True,
)


st.caption(
    "These are the documented Final V2 benchmark values. "
    "They should be regenerated whenever the dataset, "
    "features, or model version changes."
)


# ==========================================================
# VALIDATION METHOD
# ==========================================================

st.subheader("Validation Method")

st.write(
    """
AquaCast uses chronological training, validation,
and test periods.

Earlier observations are used to predict later
conditions rather than randomly mixing historical
and future observations.

Probability thresholds are selected using the
validation period only. The final test period is
reserved for final evaluation.

False negatives receive special attention because
they represent elevated-risk conditions predicted
as lower risk.
"""
)


# ==========================================================
# LIVE FORECAST EXTENSION
# ==========================================================

st.subheader("Live Forecast Extension")

st.write(
    """
The deployed BeachGuard application extends the
original AquaCast research pipeline with a live
weather support layer.

Recent and forecast weather conditions are retrieved
from Open-Meteo and transformed into the same types
of environmental features used by the trained models.

Some features that depend on previous laboratory
results use the latest available historical value,
because future laboratory measurements are not known.
"""
)


# ==========================================================
# AI-ASSISTED DEVELOPMENT
# ==========================================================

st.subheader("AI-Assisted Development")

st.write(
    """
AI-assisted tools were used for limited code support,
debugging, review, and documentation.

The project developer remains responsible for
understanding, testing, editing, debugging, and
maintaining the submitted code.
"""
)


# ==========================================================
# FOOTER
# ==========================================================

if current is not None:
    footer_version = str(
        current.get(
            "model_version",
            APP_VERSION,
        )
    )
else:
    footer_version = APP_VERSION


render_footer(
    footer_version
)
