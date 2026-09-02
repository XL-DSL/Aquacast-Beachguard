import streamlit as st

from utils.styles import apply_styles
from utils.ui import (
    OFFICIAL_URL,
    render_footer,
)


st.set_page_config(
    page_title="Limitations | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("Limitations")

st.caption(
    "Important limitations of BeachGuard / AquaCast."
)


# ==========================================================
# EXPERIMENTAL STATUS
# ==========================================================

st.warning(
    "BeachGuard is an experimental research prototype "
    "and is not an official water-quality advisory."
)


# ==========================================================
# ONE PILOT SITE
# ==========================================================

st.subheader("One Pilot Site")

st.write(
    """
The current system is designed for
**Parkside Aquatic Park, San Mateo, California**.

Performance should not automatically be assumed
to transfer to other beaches, lagoons, counties,
or watersheds without additional testing and validation.
"""
)


# ==========================================================
# NOT A REAL-TIME BACTERIA SENSOR
# ==========================================================

st.subheader("Not a Real-Time Bacteria Sensor")

st.write(
    """
BeachGuard does not directly measure bacteria
in the water.

Instead, AquaCast estimates bacterial risk using
environmental conditions and relationships found
in historical monitoring data.

Laboratory testing is still required to directly
measure bacterial concentrations.
"""
)


# ==========================================================
# LIMITED ELEVATED-RISK EVENTS
# ==========================================================

st.subheader("Limited Elevated-Risk Events")

st.write(
    """
Elevated bacterial observations occur less often
than lower-risk observations in the historical dataset.

This is particularly important for **Enterococcus**,
where the number of exceedance events is relatively
limited.

Because there are fewer elevated-risk examples for
the model to learn from, Enterococcus predictions
may be less reliable under some conditions.
"""
)


# ==========================================================
# HISTORICAL RELATIONSHIPS
# ==========================================================

st.subheader("Historical Relationships Can Change")

st.write(
    """
AquaCast relies on relationships identified in
historical environmental and bacterial monitoring data.

Those relationships may not remain identical in the future.

Unexpected contamination sources, infrastructure failures,
wildlife events, unusual storms, or environmental conditions
outside the historical training range may reduce model accuracy.
"""
)


# ==========================================================
# WEATHER FORECAST UNCERTAINTY
# ==========================================================

st.subheader("Weather Forecast Uncertainty")

st.write(
    """
The live forecast extension uses recent and forecast
weather conditions.

Weather forecasts, especially rainfall forecasts,
can be inaccurate.

Because rainfall and other environmental conditions
are model inputs, weather forecast errors can affect
the resulting AquaCast bacterial-risk probabilities.
"""
)


# ==========================================================
# LATEST-KNOWN LAB VALUES
# ==========================================================

st.subheader("Latest-Known Laboratory Inputs")

st.write(
    """
Some AquaCast model features depend on previous
bacterial monitoring results.

Future laboratory measurements are not available
at prediction time.

For these features, the live forecasting layer uses
the latest available historical laboratory information.

As a result, the live forecast should be interpreted
as a decision-support estimate rather than a
laboratory-confirmed current water condition.
"""
)


# ==========================================================
# MODEL PERFORMANCE
# ==========================================================

st.subheader("Performance Can Change")

st.write(
    """
Historical test performance does not guarantee
the same performance on future observations.

Model performance should be reevaluated whenever
the dataset, feature set, thresholds, or trained
model versions change.
"""
)


# ==========================================================
# FALSE NEGATIVES
# ==========================================================

st.subheader("False Negatives Are Possible")

st.write(
    """
Like any classification model, AquaCast can make
incorrect predictions.

A particularly important error is a **false negative**:
a condition in which bacterial risk is actually elevated
but the model predicts a lower-risk category.

For this reason, AquaCast forecasts should never be used
as the only basis for deciding whether recreational water
is safe.
"""
)


# ==========================================================
# OFFICIAL INFORMATION
# ==========================================================

st.subheader("Official Information Takes Priority")

st.write(
    """
Official laboratory results, public-health advisories,
beach postings, closures, and government agency notices
always take priority over an AquaCast forecast.

BeachGuard is intended to supplement public information,
not replace it.
"""
)


# ==========================================================
# OFFICIAL ADVISORY BUTTON
# ==========================================================

st.link_button(
    "Check Official Water-Quality Advisories",
    OFFICIAL_URL,
    use_container_width=True,
)


# ==========================================================
# FOOTER
# ==========================================================

render_footer()
