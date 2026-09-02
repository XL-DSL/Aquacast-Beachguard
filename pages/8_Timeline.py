import pandas as pd
import streamlit as st

from utils.live_forecast import (
    load_live_outlook,
)
from utils.styles import (
    apply_styles,
)
from utils.ui import (
    OFFICIAL_URL,
    SITE_NAME,
    render_footer,
    risk_class,
    risk_icon,
)


st.set_page_config(
    page_title="7-Day Forecast | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "7-Day Forecast"
)

st.caption(
    "Experimental AquaCast water-quality risk outlook "
    f"for the next seven days at {SITE_NAME}."
)


# ==========================================================
# LOAD TODAY + NEXT 7 DAYS
# ==========================================================

try:
    with st.spinner(
        "Generating 7-day AquaCast outlook..."
    ):
        outlook = (
            load_live_outlook(
                days=8
            )
        )

except Exception:
    st.error(
        "The 7-day forecast is "
        "temporarily unavailable."
    )

    st.link_button(
        "Check Official Water-Quality Advisories",
        OFFICIAL_URL,
        use_container_width=True,
    )

    st.stop()


# ==========================================================
# PREPARE FUTURE DATES
# ==========================================================

outlook = (
    outlook.copy()
)

outlook[
    "prediction_date"
] = pd.to_datetime(
    outlook[
        "prediction_date"
    ],
    errors="coerce",
)


outlook = (
    outlook
    .dropna(
        subset=[
            "prediction_date"
        ]
    )
)


today = (
    pd.Timestamp.today()
    .normalize()
)


future = (
    outlook[
        outlook[
            "prediction_date"
        ]
        .dt.normalize()
        > today
    ]
    .sort_values(
        "prediction_date"
    )
    .head(
        7
    )
    .reset_index(
        drop=True
    )
)


if future.empty:
    st.error(
        "No future AquaCast forecast "
        "dates are currently available."
    )

    st.stop()


# ==========================================================
# FORECAST INFORMATION
# ==========================================================

st.html(
    """
<div style="
    background:#EFF6FF;
    color:#344054;
    border-left:4px solid #0F6B78;
    border-radius:0 12px 12px 0;
    padding:1rem 1.1rem;
    margin-bottom:1.5rem;
    line-height:1.6;
">
    <strong>How to read this forecast</strong><br>
    Each day shows AquaCast's predicted probability
    that E. coli and Enterococcus exceed their
    elevated-risk concentration thresholds.
    Forecast uncertainty generally increases farther
    into the future because weather forecasts can change.
</div>
"""
)


# ==========================================================
# FORECAST TIMELINE
# ==========================================================

st.subheader(
    "Forecast Timeline"
)


for index, row in (
    future.iterrows()
):

    prediction_date = (
        pd.to_datetime(
            row[
                "prediction_date"
            ]
        )
    )

    day_name = (
        prediction_date
        .strftime(
            "%A"
        )
    )

    date_text = (
        prediction_date
        .strftime(
            "%b %d"
        )
    )


    ecoli_prob = float(
        row[
            "e_coli_probability"
        ]
    )

    entero_prob = float(
        row[
            "enterococcus_probability"
        ]
    )


    ecoli_risk = str(
        row[
            "e_coli_risk"
        ]
    ).strip()

    entero_risk = str(
        row[
            "enterococcus_risk"
        ]
    ).strip()

    overall = str(
        row[
            "overall_risk"
        ]
    ).strip()


    css_class = (
        risk_class(
            overall
        )
    )

    icon = (
        risk_icon(
            overall
        )
    )


    if index == 0:
        day_label = (
            "Tomorrow"
        )

    else:
        day_label = (
            day_name
        )


    st.html(
        f"""
<div class="timeline-card {css_class}">

    <div class="timeline-left">

        <div class="timeline-date">
            {day_label}
        </div>

        <div class="timeline-date-small">
            {date_text}
        </div>

    </div>


    <div class="timeline-status">

        <div class="timeline-status-icon">
            {icon}
        </div>

        <div>

            <div class="timeline-risk {css_class}">
                {overall}
            </div>

            <div class="timeline-risk-label">
                Overall AquaCast risk
            </div>

        </div>

    </div>


    <div class="timeline-bacteria">

        <div class="timeline-bacteria-item">

            <span class="timeline-bacteria-name">
                E. coli
            </span>

            <strong>
                {ecoli_prob:.0%}
            </strong>

            <span class="timeline-small-risk {risk_class(ecoli_risk)}">
                {ecoli_risk}
            </span>

        </div>


        <div class="timeline-bacteria-item">

            <span class="timeline-bacteria-name">
                Enterococcus
            </span>

            <strong>
                {entero_prob:.0%}
            </strong>

            <span class="timeline-small-risk {risk_class(entero_risk)}">
                {entero_risk}
            </span>

        </div>

    </div>

</div>
"""
    )


# ==========================================================
# FORECAST TABLE
# ==========================================================

st.subheader(
    "7-Day Forecast Details"
)


display = future[
    [
        "prediction_date",
        "e_coli_probability",
        "e_coli_risk",
        "enterococcus_probability",
        "enterococcus_risk",
        "overall_risk",
    ]
].copy()


display[
    "prediction_date"
] = (
    display[
        "prediction_date"
    ]
    .dt.strftime(
        "%a, %b %d"
    )
)


display[
    "e_coli_probability"
] = (
    display[
        "e_coli_probability"
    ]
    .map(
        lambda value:
            f"{float(value):.0%}"
    )
)


display[
    "enterococcus_probability"
] = (
    display[
        "enterococcus_probability"
    ]
    .map(
        lambda value:
            f"{float(value):.0%}"
    )
)


display.columns = [
    "Date",
    "E. coli Probability",
    "E. coli Risk",
    "Enterococcus Probability",
    "Enterococcus Risk",
    "Overall Risk",
]


st.dataframe(
    display,
    hide_index=True,
    use_container_width=True,
)


# ==========================================================
# FORECAST LIMITATION
# ==========================================================

st.html(
    """
<div style="
    background:#FFF8CC;
    color:#5C4A00;
    border:1px solid #F1E59A;
    border-radius:12px;
    padding:1rem 1.1rem;
    margin-top:1rem;
    margin-bottom:1.5rem;
    line-height:1.6;
">
    <strong>Experimental forecast:</strong>
    These predictions are not laboratory measurements
    or official water-quality advisories.
    Weather forecasts and AquaCast risk estimates may
    change as new information becomes available.
</div>
"""
)


# ==========================================================
# OFFICIAL ADVISORY
# ==========================================================

st.link_button(
    "Check Official Water-Quality Advisories",
    OFFICIAL_URL,
    use_container_width=True,
)


# ==========================================================
# FOOTER
# ==========================================================

if (
    "model_version"
    in future.columns
):
    model_version = str(
        future.iloc[0][
            "model_version"
        ]
    )

else:
    model_version = None


render_footer(
    model_version
)
