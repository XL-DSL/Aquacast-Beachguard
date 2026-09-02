import pandas as pd
import streamlit as st

from utils.live_forecast import load_live_latest
from utils.styles import apply_styles
from utils.ui import (
    SITE_NAME,
    OFFICIAL_URL,
    render_footer,
)
from utils.validation import load_valid_latest


st.set_page_config(
    page_title="Pilot Site Map | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


SITE_LAT = 37.5602
SITE_LON = -122.2910


# ==========================================================
# LOAD CURRENT PREDICTION
# ==========================================================

live_prediction = True

try:
    latest = load_live_latest()

except Exception:
    live_prediction = False

    try:
        latest = load_valid_latest()

    except Exception:
        st.error(
            "Map data is currently unavailable."
        )

        st.link_button(
            "Check Official Water-Quality Advisories",
            OFFICIAL_URL,
        )

        st.stop()


# ==========================================================
# PREPARE VALUES
# ==========================================================

latitude = float(
    latest.get(
        "latitude",
        SITE_LAT,
    )
)

longitude = float(
    latest.get(
        "longitude",
        SITE_LON,
    )
)

overall_risk = str(
    latest["overall_risk"]
).strip()

prediction_date = pd.to_datetime(
    latest["prediction_date"],
    errors="coerce",
)

model_version = str(
    latest["model_version"]
)

prediction_text = (
    prediction_date.strftime(
        "%b %d, %Y"
    )
    if pd.notna(prediction_date)
    else "Date unavailable"
)

source_text = (
    "Live AquaCast forecast"
    if live_prediction
    else "Latest validated saved forecast"
)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "Pilot Site Map"
)

st.caption(
    f"{SITE_NAME} · "
    "San Mateo, California"
)


# ==========================================================
# CURRENT SITE STATUS
# ==========================================================

col1, col2, col3 = st.columns(
    3
)

with col1:
    st.metric(
        "Current Overall Risk",
        overall_risk,
    )

with col2:
    st.metric(
        "Prediction Date",
        prediction_text,
    )

with col3:
    st.metric(
        "Forecast Source",
        (
            "Live"
            if live_prediction
            else "Saved"
        ),
    )


# ==========================================================
# MAP
# ==========================================================

map_data = pd.DataFrame(
    {
        "lat": [
            latitude
        ],
        "lon": [
            longitude
        ],
    }
)

with st.container(
    border=True
):
    st.map(
        map_data,
        zoom=14,
    )

    st.caption(
        f"📍 {SITE_NAME} · "
        f"Current AquaCast risk: {overall_risk}"
    )


# ==========================================================
# SITE INFORMATION
# ==========================================================

st.subheader(
    "Site Information"
)

info_col1, info_col2 = st.columns(
    2
)

with info_col1:
    st.markdown(
        f"""
**Pilot site:** {SITE_NAME}

**Latitude:** {latitude:.4f}

**Longitude:** {longitude:.4f}
"""
    )

with info_col2:
    st.markdown(
        f"""
**Current model risk:** {overall_risk}

**Forecast date:** {prediction_text}

**Data source:** {source_text}
"""
    )


# ==========================================================
# MAP LINKS
# ==========================================================

button_col1, button_col2 = st.columns(
    2
)

with button_col1:
    st.link_button(
        "Open in Google Maps",
        (
            "https://www.google.com/maps/search/"
            "?api=1&query="
            f"{latitude},{longitude}"
        ),
        use_container_width=True,
    )

with button_col2:
    st.link_button(
        "Check Official Advisories",
        OFFICIAL_URL,
        use_container_width=True,
    )


# ==========================================================
# SAFETY NOTE
# ==========================================================

st.warning(
    "This map identifies the AquaCast pilot site "
    "and displays a model-estimated risk. "
    "It does not represent an official beach closure, "
    "posting, or public-health advisory."
)


# ==========================================================
# FOOTER
# ==========================================================

render_footer(
    model_version
)
