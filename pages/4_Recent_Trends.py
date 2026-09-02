import altair as alt
import pandas as pd
import streamlit as st

from utils.live_forecast import load_recent_estimates
from utils.styles import apply_styles
from utils.ui import render_footer


st.set_page_config(
    page_title="Recent Trends | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


st.title("Recent Trends")

st.caption(
    "Recent AquaCast model-estimated bacterial "
    "exceedance probabilities for Parkside Aquatic Park."
)


days = st.select_slider(
    "Trend window",
    options=[7, 14, 21, 30],
    value=14,
    format_func=lambda value: f"{value} days",
)


try:
    with st.spinner("Loading recent estimates..."):
        trends = load_recent_estimates(days)

except Exception:
    st.error(
        "Recent trend data is temporarily unavailable."
    )
    st.stop()


# ==========================================================
# PREPARE CHART DATA
# ==========================================================

chart_data = trends[
    [
        "prediction_date",
        "e_coli_probability",
        "enterococcus_probability",
    ]
].copy()


chart_data["prediction_date"] = pd.to_datetime(
    chart_data["prediction_date"],
    errors="coerce",
)


chart_data = chart_data.dropna(
    subset=["prediction_date"]
)


chart_data = chart_data.melt(
    id_vars=["prediction_date"],
    value_vars=[
        "e_coli_probability",
        "enterococcus_probability",
    ],
    var_name="Bacterium",
    value_name="Probability",
)


chart_data["Bacterium"] = chart_data[
    "Bacterium"
].replace(
    {
        "e_coli_probability": "E. coli",
        "enterococcus_probability": "Enterococcus",
    }
)


chart_data["Probability (%)"] = (
    chart_data["Probability"] * 100
)


# ==========================================================
# TREND CHART
# ==========================================================

chart = (
    alt.Chart(chart_data)
    .mark_line(
        point=True,
        strokeWidth=3,
    )
    .encode(
        x=alt.X(
            "prediction_date:T",
            title="Date",
            axis=alt.Axis(
                format="%b %d",
                labelAngle=-35,
            ),
        ),
        y=alt.Y(
            "Probability (%):Q",
            title="Predicted exceedance probability (%)",
            scale=alt.Scale(
                domain=[0, 100]
            ),
        ),
        color=alt.Color(
            "Bacterium:N",
            title="Bacterium",
        ),
        tooltip=[
            alt.Tooltip(
                "prediction_date:T",
                title="Date",
                format="%b %d, %Y",
            ),
            alt.Tooltip(
                "Bacterium:N",
                title="Bacterium",
            ),
            alt.Tooltip(
                "Probability (%):Q",
                title="Probability",
                format=".1f",
            ),
        ],
    )
    .properties(
        height=400
    )
    .interactive()
)


st.altair_chart(
    chart,
    use_container_width=True,
)


st.caption(
    "These values are model estimates, "
    "not laboratory measurements."
)


# ==========================================================
# MOST RECENT VALUES
# ==========================================================

latest = trends.iloc[-1]


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Latest E. coli Probability",
        f"{float(latest['e_coli_probability']):.0%}",
    )


with col2:
    st.metric(
        "Latest Enterococcus Probability",
        f"{float(latest['enterococcus_probability']):.0%}",
    )


with col3:
    st.metric(
        "Latest Overall Risk",
        str(latest["overall_risk"]),
    )


# ==========================================================
# TABLE
# ==========================================================

st.subheader("Daily Estimates")


display = trends.copy()


display["prediction_date"] = pd.to_datetime(
    display["prediction_date"],
    errors="coerce",
).dt.strftime(
    "%b %d, %Y"
)


display["e_coli_probability"] = display[
    "e_coli_probability"
].map(
    lambda value: f"{float(value):.0%}"
)


display["enterococcus_probability"] = display[
    "enterococcus_probability"
].map(
    lambda value: f"{float(value):.0%}"
)


display = display[
    [
        "prediction_date",
        "e_coli_probability",
        "enterococcus_probability",
        "overall_risk",
    ]
]


display.columns = [
    "Date",
    "E. coli",
    "Enterococcus",
    "Overall Risk",
]


st.dataframe(
    display.iloc[::-1],
    hide_index=True,
    use_container_width=True,
)


# ==========================================================
# EXPLANATION
# ==========================================================

st.info(
    "The chart shows AquaCast's estimated probability "
    "that each bacterial indicator exceeds its "
    "elevated-risk concentration threshold. "
    "It does not show measured bacterial concentrations."
)


# ==========================================================
# FOOTER
# ==========================================================

render_footer()
