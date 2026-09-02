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
    page_title="15-Day Timeline | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


# ==========================================================
# PAGE-SPECIFIC TIMELINE STYLING
# ==========================================================

st.html(
    """
<style>

/* ==========================================================
   15-DAY AQUACAST TIMELINE
   7 past days + today + 7 future days
   ========================================================== */

.timeline-intro {
    color: #667085;
    font-size: 0.92rem;
    margin-bottom: 1.25rem;
}


/* ----------------------------------------------------------
   LEGEND
   ---------------------------------------------------------- */

.timeline-period-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;

    margin-bottom: 1.5rem;
}

.timeline-period-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;

    padding: 0.35rem 0.7rem;

    border-radius: 999px;

    font-size: 0.72rem;
    font-weight: 700;
}

.timeline-period-chip.past {
    background: #F2F4F7;
    color: #667085;
}

.timeline-period-chip.today {
    background: #E6F4F5;
    color: #0F6B78;
}

.timeline-period-chip.future {
    background: #EEF4FF;
    color: #344F8A;
}


/* ----------------------------------------------------------
   TIMELINE
   ---------------------------------------------------------- */

.aquacast-timeline {
    position: relative;

    margin-top: 0.5rem;
    margin-bottom: 2rem;
}


/* Vertical line */

.aquacast-timeline::before {
    content: "";

    position: absolute;

    left: 108px;
    top: 28px;
    bottom: 28px;

    width: 3px;

    background: #DDE3EA;

    border-radius: 999px;
}


/* ----------------------------------------------------------
   ONE DAY
   ---------------------------------------------------------- */

.timeline-day {
    position: relative;

    display: grid;

    grid-template-columns:
        86px
        42px
        minmax(0, 1fr);

    align-items: center;

    gap: 0.65rem;

    margin-bottom: 0.8rem;
}


/* Date */

.timeline-day-label {
    text-align: right;
}

.timeline-day-name {
    color: #172033;

    font-size: 0.88rem;
    font-weight: 800;
}

.timeline-day-date {
    color: #98A2B3;

    margin-top: 0.1rem;

    font-size: 0.7rem;
}


/* ----------------------------------------------------------
   TIMELINE DOT
   ---------------------------------------------------------- */

.timeline-dot-wrap {
    position: relative;

    display: flex;
    justify-content: center;

    z-index: 2;
}

.timeline-dot {
    width: 22px;
    height: 22px;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 4px solid #F5F7FA;

    border-radius: 50%;

    color: #FFFFFF;

    font-size: 0.62rem;
    font-weight: 800;
}

.timeline-dot.safe {
    background: #2E7D32;
}

.timeline-dot.caution {
    background: #B26A00;
}

.timeline-dot.unsafe {
    background: #C62828;
}


/* Today gets a larger ring */

.timeline-dot.today {
    width: 28px;
    height: 28px;

    border: 5px solid #D6EFF1;

    box-shadow:
        0 0 0 2px #0F6B78;
}


/* ----------------------------------------------------------
   DAY CARD
   ---------------------------------------------------------- */

.timeline-card {
    display: grid;

    grid-template-columns:
        145px
        repeat(2, minmax(120px, 1fr));

    align-items: center;

    gap: 0.8rem;

    background: #FFFFFF;

    border: 1px solid #E4E7EC;
    border-left: 5px solid #98A2B3;

    border-radius: 13px;

    padding: 0.85rem 1rem;

    box-shadow:
        0 1px 4px rgba(16, 24, 40, 0.04);
}


/* Risk border */

.timeline-card.safe {
    border-left-color: #2E7D32;
}

.timeline-card.caution {
    border-left-color: #B26A00;
}

.timeline-card.unsafe {
    border-left-color: #C62828;
}


/* Past days slightly muted */

.timeline-card.past {
    background: #FBFCFD;
}


/* Today emphasized */

.timeline-card.today {
    border: 2px solid #0F6B78;

    box-shadow:
        0 3px 12px rgba(15, 107, 120, 0.10);
}


/* Future */

.timeline-card.future {
    background: #FFFFFF;
}


/* ----------------------------------------------------------
   OVERALL STATUS
   ---------------------------------------------------------- */

.timeline-overall {
    min-width: 0;
}

.timeline-period-label {
    color: #98A2B3;

    margin-bottom: 0.15rem;

    font-size: 0.62rem;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.timeline-overall-value {
    font-size: 1.05rem;
    font-weight: 800;
}

.timeline-overall-value.safe {
    color: #2E7D32;
}

.timeline-overall-value.caution {
    color: #B26A00;
}

.timeline-overall-value.unsafe {
    color: #C62828;
}


/* ----------------------------------------------------------
   BACTERIA BOXES
   ---------------------------------------------------------- */

.timeline-bacteria {
    background: #F8FAFC;

    border-radius: 9px;

    padding: 0.55rem 0.7rem;
}

.timeline-bacteria-top {
    display: flex;

    align-items: center;
    justify-content: space-between;

    gap: 0.5rem;
}

.timeline-bacteria-name {
    color: #667085;

    font-size: 0.72rem;
    font-weight: 600;
}

.timeline-bacteria-value {
    color: #172033;

    font-size: 0.92rem;
    font-weight: 800;
}

.timeline-bacteria-risk {
    margin-top: 0.1rem;

    font-size: 0.65rem;
    font-weight: 700;
}

.timeline-bacteria-risk.safe {
    color: #2E7D32;
}

.timeline-bacteria-risk.caution {
    color: #B26A00;
}

.timeline-bacteria-risk.unsafe {
    color: #C62828;
}


/* ----------------------------------------------------------
   TODAY LABEL
   ---------------------------------------------------------- */

.today-badge {
    display: inline-flex;

    margin-left: 0.35rem;

    padding: 0.15rem 0.4rem;

    border-radius: 999px;

    background: #0F6B78;

    color: #FFFFFF;

    font-size: 0.58rem;
    font-weight: 800;

    vertical-align: middle;
}


/* ----------------------------------------------------------
   RISK LEGEND
   ---------------------------------------------------------- */

.timeline-risk-legend {
    display: flex;
    flex-wrap: wrap;

    gap: 1rem;

    margin:
        0.4rem
        0
        1.5rem
        132px;

    color: #667085;

    font-size: 0.72rem;
}

.timeline-risk-item {
    display: flex;
    align-items: center;

    gap: 0.35rem;
}

.timeline-risk-dot {
    width: 9px;
    height: 9px;

    border-radius: 50%;
}

.timeline-risk-dot.safe {
    background: #2E7D32;
}

.timeline-risk-dot.caution {
    background: #B26A00;
}

.timeline-risk-dot.unsafe {
    background: #C62828;
}


/* ----------------------------------------------------------
   MOBILE
   ---------------------------------------------------------- */

@media (max-width: 720px) {

    .aquacast-timeline::before {
        left: 18px;
    }

    .timeline-day {
        grid-template-columns:
            36px
            minmax(0, 1fr);

        gap: 0.45rem;
    }

    .timeline-day-label {
        grid-column: 2;

        text-align: left;

        margin-bottom: -0.25rem;
    }

    .timeline-dot-wrap {
        grid-column: 1;

        grid-row:
            1
            / span 2;
    }

    .timeline-card {
        grid-column: 2;

        grid-template-columns: 1fr;

        gap: 0.55rem;
    }

    .timeline-risk-legend {
        margin-left: 44px;
    }

}

</style>
"""
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "15-Day AquaCast Timeline"
)

st.html(
    f"""
<div class="timeline-intro">
    Recent conditions, today's AquaCast result,
    and the next seven days at
    <strong>{SITE_NAME}</strong>.
</div>

<div class="timeline-period-legend">

    <span class="timeline-period-chip past">
        Previous 7 Days
    </span>

    <span class="timeline-period-chip today">
        Today
    </span>

    <span class="timeline-period-chip future">
        Next 7 Days
    </span>

</div>
"""
)


# ==========================================================
# LOAD PAST + CURRENT + FUTURE
# ==========================================================

try:

    with st.spinner(
        "Building AquaCast timeline..."
    ):

        # Returns recent estimates ending with today.
        recent = load_recent_estimates(
            days=8
        )

        # Returns today + next seven days.
        outlook = load_live_outlook(
            days=8
        )

except Exception:

    st.error(
        "The AquaCast timeline is "
        "temporarily unavailable."
    )

    st.link_button(
        "Check Official Water-Quality Advisories",
        OFFICIAL_URL,
        use_container_width=True,
    )

    st.stop()


# ==========================================================
# CLEAN DATES
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
    .tz_localize(None)
    .normalize()
)


# ==========================================================
# PREVIOUS 7 DAYS
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
    .tail(7)
    .copy()
)


past[
    "period"
] = "past"


# ==========================================================
# TODAY
# Use the LIVE outlook value so today's number matches
# the Current Forecast page.
# ==========================================================

current = (
    outlook[
        outlook[
            "prediction_date"
        ]
        .dt.normalize()
        == today
    ]
    .head(1)
    .copy()
)


if current.empty:

    # Fallback to today's recent estimate if necessary.
    current = (
        recent[
            recent[
                "prediction_date"
            ]
            .dt.normalize()
            == today
        ]
        .tail(1)
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
    .head(7)
    .copy()
)


future[
    "period"
] = "future"


# ==========================================================
# COMBINE
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
# RISK LEGEND
# ==========================================================

st.html(
    """
<div class="timeline-risk-legend">

    <div class="timeline-risk-item">
        <span class="timeline-risk-dot safe"></span>
        Safe
    </div>

    <div class="timeline-risk-item">
        <span class="timeline-risk-dot caution"></span>
        Caution
    </div>

    <div class="timeline-risk-item">
        <span class="timeline-risk-dot unsafe"></span>
        Unsafe
    </div>

</div>
"""
)


# ==========================================================
# BUILD TIMELINE
# ==========================================================

timeline_html = """
<div class="aquacast-timeline">
"""


for _, row in timeline.iterrows():

    forecast_date = pd.to_datetime(
        row[
            "prediction_date"
        ]
    )


    period = str(
        row[
            "period"
        ]
    )


    day_name = (
        forecast_date.strftime(
            "%A"
        )
    )


    date_text = (
        forecast_date.strftime(
            "%b %d"
        )
    )


    # ------------------------------------------------------
    # Friendly day labels
    # ------------------------------------------------------

    day_difference = (
        forecast_date.normalize()
        - today
    ).days


    if day_difference == 0:

        display_day = (
            "Today"
        )

        today_badge = (
            '<span class="today-badge">'
            'CURRENT'
            '</span>'
        )


    elif day_difference == 1:

        display_day = (
            "Tomorrow"
        )

        today_badge = ""


    elif day_difference == -1:

        display_day = (
            "Yesterday"
        )

        today_badge = ""


    else:

        display_day = (
            day_name
        )

        today_badge = ""


    # ------------------------------------------------------
    # Values
    # ------------------------------------------------------

    ecoli_probability = float(
        row[
            "e_coli_probability"
        ]
    )


    enterococcus_probability = float(
        row[
            "enterococcus_probability"
        ]
    )


    ecoli_risk = str(
        row[
            "e_coli_risk"
        ]
    ).strip()


    enterococcus_risk = str(
        row[
            "enterococcus_risk"
        ]
    ).strip()


    overall = str(
        row[
            "overall_risk"
        ]
    ).strip()


    overall_class = (
        risk_class(
            overall
        )
    )


    ecoli_class = (
        risk_class(
            ecoli_risk
        )
    )


    entero_class = (
        risk_class(
            enterococcus_risk
        )
    )


    icon = (
        risk_icon(
            overall
        )
    )


    # ------------------------------------------------------
    # Period label
    # ------------------------------------------------------

    if period == "past":

        period_label = (
            "Recent Estimate"
        )


    elif period == "today":

        period_label = (
            "Current Forecast"
        )


    else:

        period_label = (
            "Future Forecast"
        )


    # ------------------------------------------------------
    # Dot class
    # ------------------------------------------------------

    dot_extra = (
        " today"
        if period == "today"
        else ""
    )


    # ------------------------------------------------------
    # Add timeline row
    # ------------------------------------------------------

    timeline_html += f"""

<div class="timeline-day">

    <div class="timeline-day-label">

        <div class="timeline-day-name">
            {display_day}
            {today_badge}
        </div>

        <div class="timeline-day-date">
            {date_text}
        </div>

    </div>


    <div class="timeline-dot-wrap">

        <div class="timeline-dot {overall_class}{dot_extra}">
            {icon}
        </div>

    </div>


    <div class="timeline-card {overall_class} {period}">

        <div class="timeline-overall">

            <div class="timeline-period-label">
                {period_label}
            </div>

            <div class="timeline-overall-value {overall_class}">
                {overall}
            </div>

        </div>


        <div class="timeline-bacteria">

            <div class="timeline-bacteria-top">

                <span class="timeline-bacteria-name">
                    E. coli
                </span>

                <span class="timeline-bacteria-value">
                    {ecoli_probability:.0%}
                </span>

            </div>

            <div class="timeline-bacteria-risk {ecoli_class}">
                {ecoli_risk}
            </div>

        </div>


        <div class="timeline-bacteria">

            <div class="timeline-bacteria-top">

                <span class="timeline-bacteria-name">
                    Enterococcus
                </span>

                <span class="timeline-bacteria-value">
                    {enterococcus_probability:.0%}
                </span>

            </div>

            <div class="timeline-bacteria-risk {entero_class}">
                {enterococcus_risk}
            </div>

        </div>

    </div>

</div>
"""


timeline_html += """
</div>
"""


st.html(
    timeline_html
)


# ==========================================================
# DETAILED TABLE
# Keep it hidden unless the user wants it.
# ==========================================================

with st.expander(
    "View detailed 15-day table"
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
                    "Recent",

                "today":
                    "Today",

                "future":
                    "Forecast",
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
# SHORT DISCLAIMER
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
    Past values shown here are AquaCast model estimates,
    not laboratory measurements. Future uncertainty
    increases farther from today. Official advisories
    always take priority.
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
