import pandas as pd
import streamlit as st

from utils.live_forecast import (
    load_live_outlook,
    load_recent_estimates,
)
from utils.styles import apply_styles
from utils.ui import (
    OFFICIAL_URL,
    SITE_NAME,
    render_footer,
    risk_class,
    risk_icon,
)


st.set_page_config(
    page_title="Timeline | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


# ==========================================================
# PAGE-SPECIFIC STYLING
# ==========================================================

st.html(
    """
<style>

/* ==========================================================
   TIMELINE PAGE
   ========================================================== */

.timeline-page-intro {
    color: #667085;
    font-size: 0.95rem;
    line-height: 1.55;
    margin-bottom: 1.5rem;
}


/* ----------------------------------------------------------
   SECTION HEADERS
   ---------------------------------------------------------- */

.timeline-section-header {
    display: flex;
    align-items: baseline;
    gap: 0.7rem;

    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
}

.timeline-section-header h2 {
    margin: 0 !important;

    color: #172033;

    font-size: 1.15rem;
    font-weight: 800;
}

.timeline-section-header span {
    color: #98A2B3;

    font-size: 0.75rem;
}


/* ----------------------------------------------------------
   SMALL DAY TILE CONTENT
   ---------------------------------------------------------- */

.timeline-tile {
    min-height: 145px;

    display: flex;
    flex-direction: column;

    gap: 0.35rem;
}

.timeline-tile-day {
    color: #172033;

    font-size: 0.85rem;
    font-weight: 800;
}

.timeline-tile-date {
    color: #98A2B3;

    font-size: 0.68rem;

    margin-top: -0.2rem;
}

.timeline-tile-badge {
    display: inline-flex;

    width: fit-content;

    align-items: center;

    padding: 0.2rem 0.45rem;

    border-radius: 999px;

    color: #FFFFFF;

    font-size: 0.63rem;
    font-weight: 800;

    margin: 0.25rem 0;
}

.timeline-tile-badge.safe {
    background: #2E7D32;
}

.timeline-tile-badge.caution {
    background: #B26A00;
}

.timeline-tile-badge.unsafe {
    background: #C62828;
}

.timeline-tile-values {
    display: grid;

    gap: 0.2rem;

    margin-top: 0.15rem;

    color: #667085;

    font-size: 0.7rem;
}

.timeline-tile-values strong {
    color: #172033;

    font-weight: 800;
}


/* ----------------------------------------------------------
   FUTURE HORIZON
   ---------------------------------------------------------- */

.timeline-horizon {
    color: #98A2B3;

    font-size: 0.62rem;

    margin-top: 0.15rem;
}


/* ----------------------------------------------------------
   TODAY HERO
   ---------------------------------------------------------- */

.timeline-today {
    display: grid;

    grid-template-columns:
        minmax(180px, 0.8fr)
        repeat(2, minmax(150px, 1fr));

    gap: 1rem;

    align-items: center;

    background: #FFFFFF;

    border: 2px solid #0F6B78;

    border-radius: 16px;

    padding: 1.35rem 1.5rem;

    margin-bottom: 1rem;

    box-shadow:
        0 4px 16px rgba(15, 107, 120, 0.10);
}

.timeline-today-label {
    color: #0F6B78;

    font-size: 0.7rem;
    font-weight: 800;

    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.timeline-today-date {
    margin-top: 0.25rem;

    color: #172033;

    font-size: 1.15rem;
    font-weight: 800;
}

.timeline-today-risk {
    margin-top: 0.45rem;

    font-size: 1.55rem;
    font-weight: 800;
}

.timeline-today-risk.safe {
    color: #2E7D32;
}

.timeline-today-risk.caution {
    color: #B26A00;
}

.timeline-today-risk.unsafe {
    color: #C62828;
}

.timeline-today-bacteria {
    background: #F8FAFC;

    border-radius: 12px;

    padding: 0.85rem 1rem;
}

.timeline-today-bacteria-name {
    color: #667085;

    font-size: 0.75rem;
    font-weight: 600;
}

.timeline-today-bacteria-value {
    margin-top: 0.2rem;

    color: #172033;

    font-size: 1.55rem;
    font-weight: 800;
}

.timeline-today-bacteria-risk {
    margin-top: 0.1rem;

    font-size: 0.7rem;
    font-weight: 700;
}

.timeline-today-bacteria-risk.safe {
    color: #2E7D32;
}

.timeline-today-bacteria-risk.caution {
    color: #B26A00;
}

.timeline-today-bacteria-risk.unsafe {
    color: #C62828;
}


/* ----------------------------------------------------------
   SELECTED DAY DETAILS
   ---------------------------------------------------------- */

.timeline-detail {
    background: #FFFFFF;

    border: 1px solid #E4E7EC;

    border-radius: 16px;

    padding: 1.3rem 1.4rem;

    margin-top: 1.5rem;
    margin-bottom: 1.3rem;

    box-shadow:
        0 1px 5px rgba(16, 24, 40, 0.05);
}

.timeline-detail-header {
    display: flex;

    justify-content: space-between;
    align-items: flex-start;

    gap: 1rem;

    margin-bottom: 1rem;
}

.timeline-detail-period {
    color: #98A2B3;

    font-size: 0.68rem;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.timeline-detail-date {
    color: #172033;

    margin-top: 0.15rem;

    font-size: 1.2rem;
    font-weight: 800;
}

.timeline-detail-risk {
    font-size: 1.2rem;
    font-weight: 800;
}

.timeline-detail-risk.safe {
    color: #2E7D32;
}

.timeline-detail-risk.caution {
    color: #B26A00;
}

.timeline-detail-risk.unsafe {
    color: #C62828;
}

.timeline-detail-driver {
    background: #F2F4F7;

    border-radius: 10px;

    padding: 0.7rem 0.85rem;

    margin-top: 0.8rem;

    color: #475467;

    font-size: 0.8rem;
    line-height: 1.45;
}


/* ----------------------------------------------------------
   SMALL VIEW BUTTONS
   ---------------------------------------------------------- */

div[data-testid="stButton"] > button {
    width: 100% !important;

    min-height: 34px !important;

    border-radius: 8px !important;

    font-size: 0.7rem !important;

    padding: 0.25rem 0.4rem !important;
}


/* ----------------------------------------------------------
   FUTURE WARNING
   ---------------------------------------------------------- */

.timeline-future-note {
    background: #FFF8CC;

    color: #5C4A00;

    border: 1px solid #F1E59A;

    border-radius: 12px;

    padding: 0.8rem 1rem;

    margin-top: 0.8rem;
    margin-bottom: 1rem;

    font-size: 0.8rem;
    line-height: 1.5;
}


/* ----------------------------------------------------------
   MOBILE
   ---------------------------------------------------------- */

@media (max-width: 720px) {

    .timeline-today {
        grid-template-columns: 1fr;

        padding: 1.1rem;
    }

    .timeline-detail-header {
        flex-direction: column;
    }

    .timeline-tile {
        min-height: auto;
    }

}

</style>
"""
)


# ==========================================================
# HELPERS
# ==========================================================

RISK_RANK = {
    "Safe": 0,
    "Caution": 1,
    "Unsafe": 2,
}


def risk_badge_html(risk):
    css_class = risk_class(
        risk
    )

    return f"""
<span class="timeline-tile-badge {css_class}">
    {risk_icon(risk)} {risk}
</span>
"""


def risk_driver(
    ecoli_risk,
    entero_risk,
):
    ecoli_rank = RISK_RANK.get(
        ecoli_risk,
        0,
    )

    entero_rank = RISK_RANK.get(
        entero_risk,
        0,
    )

    if ecoli_rank > entero_rank:
        return (
            "Overall risk is currently driven "
            "by the E. coli prediction."
        )

    if entero_rank > ecoli_rank:
        return (
            "Overall risk is currently driven "
            "by the Enterococcus prediction."
        )

    if ecoli_rank == 0:
        return (
            "Both bacteria are currently "
            "classified as Safe."
        )

    return (
        "Both bacteria are currently at the "
        f"{ecoli_risk} risk level."
    )


def set_selected_day(
    prediction_date
):
    st.session_state[
        "timeline_selected_date"
    ] = (
        pd.Timestamp(
            prediction_date
        )
        .strftime(
            "%Y-%m-%d"
        )
    )


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "15-Day AquaCast Timeline"
)

st.html(
    f"""
<div class="timeline-page-intro">
    Seven reconstructed recent model estimates,
    today's current forecast, and seven future forecasts
    for <strong>{SITE_NAME}</strong>.
</div>
"""
)


# ==========================================================
# LOAD DATA
# ==========================================================

try:
    with st.spinner(
        "Building AquaCast timeline..."
    ):

        recent = load_recent_estimates(
            days=8
        )

        outlook = load_live_outlook(
            days=8
        )

except Exception:

    st.error(
        "The AquaCast timeline is "
        "temporarily unavailable."
    )

    st.link_button(
        "View Official San Mateo County Beach Status",
        OFFICIAL_URL,
        use_container_width=True,
    )

    st.stop()


# ==========================================================
# CLEAN DATA
# ==========================================================

recent = recent.copy()
outlook = outlook.copy()


recent[
    "prediction_date"
] = pd.to_datetime(
    recent[
        "prediction_date"
    ],
    errors="coerce",
)


outlook[
    "prediction_date"
] = pd.to_datetime(
    outlook[
        "prediction_date"
    ],
    errors="coerce",
)


recent = recent.dropna(
    subset=[
        "prediction_date"
    ]
)


outlook = outlook.dropna(
    subset=[
        "prediction_date"
    ]
)


today = (
    pd.Timestamp.now(
        tz="America/Los_Angeles"
    )
    .tz_localize(
        None
    )
    .normalize()
)


# ==========================================================
# PREVIOUS 7 DAYS
# Reconstructed model estimates, NOT saved historical forecasts.
# ==========================================================

past = (
    recent[
        recent[
            "prediction_date"
        ]
        .dt.normalize()
        < today
    ]
    .sort_values(
        "prediction_date"
    )
    .tail(
        7
    )
    .copy()
)


past[
    "period"
] = "past"


# ==========================================================
# TODAY
# Use current live forecast so this matches Current Forecast.
# ==========================================================

current = (
    outlook[
        outlook[
            "prediction_date"
        ]
        .dt.normalize()
        == today
    ]
    .head(
        1
    )
    .copy()
)


if current.empty:

    current = (
        recent[
            recent[
                "prediction_date"
            ]
            .dt.normalize()
            == today
        ]
        .tail(
            1
        )
        .copy()
    )


current[
    "period"
] = "today"


# ==========================================================
# NEXT 7 DAYS
# ==========================================================

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
    .copy()
)


future[
    "period"
] = "future"


# ==========================================================
# ALL 15 DAYS
# ==========================================================

timeline = pd.concat(
    [
        past,
        current,
        future,
    ],
    ignore_index=True,
    sort=False,
)


timeline = (
    timeline
    .sort_values(
        "prediction_date"
    )
    .reset_index(
        drop=True
    )
)


if timeline.empty:
    st.error(
        "No timeline data are currently available."
    )

    st.stop()


# ==========================================================
# DEFAULT SELECTION = TODAY
# ==========================================================

today_key = today.strftime(
    "%Y-%m-%d"
)


if (
    "timeline_selected_date"
    not in st.session_state
):
    st.session_state[
        "timeline_selected_date"
    ] = today_key


valid_keys = set(
    timeline[
        "prediction_date"
    ]
    .dt.strftime(
        "%Y-%m-%d"
    )
)


if (
    st.session_state[
        "timeline_selected_date"
    ]
    not in valid_keys
):
    st.session_state[
        "timeline_selected_date"
    ] = today_key


# ==========================================================
# PREVIOUS 7 DAYS
# ==========================================================

st.html(
    """
<div class="timeline-section-header">
    <h2>Previous 7 Days</h2>
    <span>Reconstructed model estimates</span>
</div>
"""
)


past_columns = st.columns(
    max(
        len(past),
        1,
    )
)


for column, (_, row) in zip(
    past_columns,
    past.iterrows(),
):

    with column:

        date_value = pd.to_datetime(
            row[
                "prediction_date"
            ]
        )

        overall = str(
            row[
                "overall_risk"
            ]
        ).strip()

        ecoli_probability = float(
            row[
                "e_coli_probability"
            ]
        )

        entero_probability = float(
            row[
                "enterococcus_probability"
            ]
        )


        with st.container(
            border=True
        ):

            st.html(
                f"""
<div class="timeline-tile">

    <div class="timeline-tile-day">
        {date_value.strftime("%a")}
    </div>

    <div class="timeline-tile-date">
        {date_value.strftime("%b %d")}
    </div>

    {risk_badge_html(overall)}

    <div class="timeline-tile-values">

        <div>
            E. coli
            <strong>{ecoli_probability:.0%}</strong>
        </div>

        <div>
            Entero
            <strong>{entero_probability:.0%}</strong>
        </div>

    </div>

</div>
"""
            )

            if st.button(
                "View",
                key=(
                    "past_"
                    + date_value.strftime(
                        "%Y%m%d"
                    )
                ),
            ):
                set_selected_day(
                    date_value
                )


# ==========================================================
# TODAY
# ==========================================================

st.html(
    """
<div class="timeline-section-header">
    <h2>Today</h2>
    <span>Current AquaCast forecast</span>
</div>
"""
)


if not current.empty:

    today_row = current.iloc[0]

    current_overall = str(
        today_row[
            "overall_risk"
        ]
    ).strip()

    current_ecoli_risk = str(
        today_row[
            "e_coli_risk"
        ]
    ).strip()

    current_entero_risk = str(
        today_row[
            "enterococcus_risk"
        ]
    ).strip()

    current_ecoli = float(
        today_row[
            "e_coli_probability"
        ]
    )

    current_entero = float(
        today_row[
            "enterococcus_probability"
        ]
    )

    current_class = risk_class(
        current_overall
    )


    st.html(
        f"""
<div class="timeline-today">

    <div>

        <div class="timeline-today-label">
            Current Forecast
        </div>

        <div class="timeline-today-date">
            {today.strftime("%A, %b %d")}
        </div>

        <div class="timeline-today-risk {current_class}">
            {risk_icon(current_overall)}
            {current_overall}
        </div>

    </div>


    <div class="timeline-today-bacteria">

        <div class="timeline-today-bacteria-name">
            E. coli
        </div>

        <div class="timeline-today-bacteria-value">
            {current_ecoli:.0%}
        </div>

        <div class="timeline-today-bacteria-risk {risk_class(current_ecoli_risk)}">
            {current_ecoli_risk}
        </div>

    </div>


    <div class="timeline-today-bacteria">

        <div class="timeline-today-bacteria-name">
            Enterococcus
        </div>

        <div class="timeline-today-bacteria-value">
            {current_entero:.0%}
        </div>

        <div class="timeline-today-bacteria-risk {risk_class(current_entero_risk)}">
            {current_entero_risk}
        </div>

    </div>

</div>
"""
    )


    st.caption(
        risk_driver(
            current_ecoli_risk,
            current_entero_risk,
        )
    )


    if st.button(
        "View today's full details",
        key="today_details",
    ):
        set_selected_day(
            today
        )


# ==========================================================
# NEXT 7 DAYS
# ==========================================================

st.html(
    """
<div class="timeline-section-header">
    <h2>Next 7 Days</h2>
    <span>Forecast uncertainty increases with horizon</span>
</div>
"""
)


future_columns = st.columns(
    max(
        len(future),
        1,
    )
)


for column, (_, row) in zip(
    future_columns,
    future.iterrows(),
):

    with column:

        date_value = pd.to_datetime(
            row[
                "prediction_date"
            ]
        )

        overall = str(
            row[
                "overall_risk"
            ]
        ).strip()

        ecoli_probability = float(
            row[
                "e_coli_probability"
            ]
        )

        entero_probability = float(
            row[
                "enterococcus_probability"
            ]
        )

        horizon = (
            date_value.normalize()
            - today
        ).days


        with st.container(
            border=True
        ):

            st.html(
                f"""
<div class="timeline-tile">

    <div class="timeline-tile-day">
        {date_value.strftime("%a")}
    </div>

    <div class="timeline-tile-date">
        {date_value.strftime("%b %d")}
    </div>

    {risk_badge_html(overall)}

    <div class="timeline-tile-values">

        <div>
            E. coli
            <strong>{ecoli_probability:.0%}</strong>
        </div>

        <div>
            Entero
            <strong>{entero_probability:.0%}</strong>
        </div>

    </div>

    <div class="timeline-horizon">
        {horizon} day{"s" if horizon != 1 else ""} ahead
    </div>

</div>
"""
            )

            if st.button(
                "View",
                key=(
                    "future_"
                    + date_value.strftime(
                        "%Y%m%d"
                    )
                ),
            ):
                set_selected_day(
                    date_value
                )


st.html(
    """
<div class="timeline-future-note">
    <strong>Future forecast:</strong>
    uncertainty increases farther from today because
    future rainfall, temperature, and other environmental
    conditions are themselves forecasted.
</div>
"""
)


# ==========================================================
# SELECTED DAY DETAILS
# ==========================================================

selected_key = st.session_state[
    "timeline_selected_date"
]


selected_rows = timeline[
    timeline[
        "prediction_date"
    ]
    .dt.strftime(
        "%Y-%m-%d"
    )
    == selected_key
]


if not selected_rows.empty:

    selected = selected_rows.iloc[0]

    selected_date = pd.to_datetime(
        selected[
            "prediction_date"
        ]
    )

    selected_period = str(
        selected[
            "period"
        ]
    )

    selected_overall = str(
        selected[
            "overall_risk"
        ]
    ).strip()

    selected_ecoli_risk = str(
        selected[
            "e_coli_risk"
        ]
    ).strip()

    selected_entero_risk = str(
        selected[
            "enterococcus_risk"
        ]
    ).strip()

    selected_ecoli = float(
        selected[
            "e_coli_probability"
        ]
    )

    selected_entero = float(
        selected[
            "enterococcus_probability"
        ]
    )


    if selected_period == "past":
        period_text = (
            "Reconstructed Recent Estimate"
        )

    elif selected_period == "today":
        period_text = (
            "Current Forecast"
        )

    else:
        horizon = (
            selected_date.normalize()
            - today
        ).days

        period_text = (
            f"Future Forecast · "
            f"{horizon} day"
            f"{'s' if horizon != 1 else ''} ahead"
        )


    st.html(
        """
<div class="timeline-section-header">
    <h2>Selected Day</h2>
    <span>Full bacteria-specific breakdown</span>
</div>
"""
    )


    st.html(
        f"""
<div class="timeline-detail">

    <div class="timeline-detail-header">

        <div>

            <div class="timeline-detail-period">
                {period_text}
            </div>

            <div class="timeline-detail-date">
                {selected_date.strftime("%A, %B %d, %Y")}
            </div>

        </div>

        <div class="timeline-detail-risk {risk_class(selected_overall)}">
            {risk_icon(selected_overall)}
            {selected_overall}
        </div>

    </div>

    <div class="timeline-detail-driver">
        {risk_driver(
            selected_ecoli_risk,
            selected_entero_risk,
        )}
    </div>

</div>
"""
    )


    detail_col1, detail_col2 = st.columns(
        2
    )


    with detail_col1:

        st.metric(
            "E. coli Probability",
            f"{selected_ecoli:.1%}",
        )

        st.caption(
            f"Risk classification: "
            f"{selected_ecoli_risk}"
        )


    with detail_col2:

        st.metric(
            "Enterococcus Probability",
            f"{selected_entero:.1%}",
        )

        st.caption(
            f"Risk classification: "
            f"{selected_entero_risk}"
        )


# ==========================================================
# DETAILED TABLE
# ==========================================================

with st.expander(
    "View all 15 daily values"
):

    display = timeline[
        [
            "prediction_date",
            "period",
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
        "period"
    ] = (
        display[
            "period"
        ]
        .replace(
            {
                "past":
                    "Reconstructed estimate",

                "today":
                    "Today",

                "future":
                    "Future forecast",
            }
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
                f"{float(value):.1%}"
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
                f"{float(value):.1%}"
        )
    )


    display.columns = [
        "Date",
        "Period",
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
# SAFETY NOTE
# ==========================================================

st.html(
    """
<div style="
    background:#FFF8CC;
    color:#5C4A00;
    border:1px solid #F1E59A;
    border-radius:12px;
    padding:0.85rem 1rem;
    margin-top:1.3rem;
    margin-bottom:1rem;
    font-size:0.82rem;
    line-height:1.5;
">
    <strong>Experimental model estimates.</strong>
    Previous-day values shown here are reconstructed
    AquaCast estimates rather than laboratory measurements
    or forecasts saved on those dates. Future forecast
    uncertainty increases with forecast horizon.
</div>
"""
)


st.link_button(
    "View Official San Mateo County Beach Status",
    OFFICIAL_URL,
    use_container_width=True,
)


# ==========================================================
# FOOTER
# ==========================================================

model_version = None


if (
    not current.empty
    and "model_version"
    in current.columns
):
    model_version = str(
        current.iloc[0][
            "model_version"
        ]
    )


render_footer(
    model_version
)
