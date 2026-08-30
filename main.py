import streamlit as st
import pandas as pd
from datetime import date

from utils.styles import (
    apply_styles,
    load_latest,
    render_hero,
    badge,
)

from utils.live_forecast import (
    load_live_latest,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BeachGuard | AquaCast Water Quality Forecast",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()


# ============================================================
# QUICK UI / DESIGN POLISH
# ============================================================

st.html(
    """
<style>

    /* ======================================================
       BEACHGUARD DESIGN TOKENS
       ====================================================== */

    :root {
        --bg-brand: #0F6B78;
        --bg-brand-hover: #0C5963;
        --bg-text: #172033;
        --bg-muted: #667085;
        --bg-border: #E4E7EC;
        --bg-surface: #FFFFFF;

        --bg-safe: #2E7D32;
        --bg-caution: #C47F00;
        --bg-unsafe: #C62828;

        --bg-radius: 16px;
        --bg-shadow: 0 2px 10px rgba(16, 24, 40, 0.06);
    }


    /* ======================================================
       PAGE WIDTH
       ====================================================== */

    .block-container {
        max-width: 1180px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 2rem !important;
    }

    .bg-content {
        max-width: 1060px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }


    /* ======================================================
       HERO
       Make the status prominent without taking over the page
       ====================================================== */

    .bg-hero {
        padding-top: 1.7rem !important;
        padding-bottom: 1.7rem !important;
        min-height: 0 !important;
    }

    .bg-hero-label {
        margin-top: 0.15rem !important;
        margin-bottom: 0.35rem !important;
    }

    .bg-hero-message {
        max-width: 680px !important;
        line-height: 1.5 !important;
    }


    /* ======================================================
       CONSISTENT CARDS
       ====================================================== */

    .bg-card,
    .bg-stat,
    .bg-detail-card,
    .bg-explainer,
    .bg-data-notes,
    .bg-disclaimer-box {
        border-radius: var(--bg-radius) !important;
        box-shadow: var(--bg-shadow) !important;
    }

    .bg-card {
        padding: 1.45rem !important;
    }

    .bg-stat {
        padding: 1rem 1.15rem !important;
    }


    /* ======================================================
       TYPOGRAPHY
       ====================================================== */

    .bg-section-header {
        font-size: 1.18rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        text-transform: none !important;
        color: var(--bg-text) !important;
        margin-top: 2.2rem !important;
        margin-bottom: 1rem !important;
    }

    .bg-stat-label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        color: var(--bg-muted) !important;
    }

    .bg-stat-value {
        color: var(--bg-text) !important;
        font-weight: 700 !important;
    }

    .bg-card-name {
        font-size: 1.08rem !important;
        font-weight: 800 !important;
        color: var(--bg-text) !important;
    }

    .bg-card-prob {
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
    }

    .bg-card-sublabel {
        font-size: 0.86rem !important;
        color: var(--bg-muted) !important;
    }

    .bg-card-threshold {
        font-size: 0.83rem !important;
        line-height: 1.55 !important;
        color: var(--bg-muted) !important;
    }


    /* ======================================================
       SECTION SPACING
       ====================================================== */

    .bg-stat-row {
        gap: 0.9rem !important;
        margin-bottom: 0.75rem !important;
    }

    .bg-card-row {
        gap: 1rem !important;
    }

    .bg-explainer {
        margin-top: 1rem !important;
    }


    /* ======================================================
       FRESHNESS CHIP
       ====================================================== */

    .bg-freshness {
        width: fit-content !important;
        border-radius: 999px !important;
        padding: 0.38rem 0.72rem !important;
        margin-top: 0.8rem !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }

    .bg-freshness.current {
        background: #F2F4F7 !important;
        color: #475467 !important;
        border: 1px solid #E4E7EC !important;
    }

    .bg-freshness.warn {
        background: #FFF7E0 !important;
        color: #8A5A00 !important;
        border: 1px solid #F0D28A !important;
    }

    .bg-freshness.error {
        background: #FDECEC !important;
        color: #A61B1B !important;
        border: 1px solid #F5BBBB !important;
    }


    /* ======================================================
       PRIMARY ACTION
       Teal is used for generic actions so green remains
       associated specifically with lower-risk status.
       ====================================================== */

    div[data-testid="stLinkButton"] a {
        background: var(--bg-brand) !important;
        border: 1px solid var(--bg-brand) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 44px !important;
        padding: 0.65rem 1.1rem !important;
        transition:
            background 0.15s ease,
            transform 0.15s ease !important;
    }

    div[data-testid="stLinkButton"] a:hover {
        background: var(--bg-brand-hover) !important;
        border-color: var(--bg-brand-hover) !important;
        transform: translateY(-1px);
    }


    /* ======================================================
       MAP CARD
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: var(--bg-radius) !important;
        border-color: var(--bg-border) !important;
        box-shadow: var(--bg-shadow) !important;
        background: white !important;
    }

    .bg-map-title {
        margin: 0 !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        color: var(--bg-text) !important;
    }

    .bg-map-subtitle {
        margin: 0.2rem 0 0.8rem 0 !important;
        color: var(--bg-muted) !important;
        font-size: 0.84rem !important;
    }

    .bg-map-label {
        max-width: 1060px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        color: var(--bg-muted) !important;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .bg-footer {
        margin-top: 2.5rem !important;
        padding-top: 1.25rem !important;
        padding-bottom: 1rem !important;
        border-top: 1px solid var(--bg-border) !important;
        color: var(--bg-muted) !important;
        font-size: 0.78rem !important;
        line-height: 1.6 !important;
    }

    .bg-footer a {
        color: var(--bg-brand) !important;
        text-decoration: none !important;
        font-weight: 600 !important;
    }

    .bg-footer a:hover {
        text-decoration: underline !important;
    }


    /* ======================================================
       MOBILE
       Same website — just rearrange the same components.
       ====================================================== */

    @media (max-width: 640px) {

        .block-container {
            width: 100% !important;
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
            padding-top: 0.75rem !important;
        }

        .bg-content {
            width: 100% !important;
            padding-left: 0.35rem !important;
            padding-right: 0.35rem !important;
        }

        .bg-hero {
            padding: 1.4rem 0.85rem !important;
        }

        .bg-hero-label {
            font-size: 2.3rem !important;
        }

        .bg-hero-message {
            font-size: 0.92rem !important;
        }

        .bg-stat-row {
            flex-direction: column !important;
            gap: 0.65rem !important;
        }

        .bg-stat {
            width: 100% !important;
        }

        .bg-card-row {
            flex-direction: column !important;
            gap: 0.85rem !important;
        }

        .bg-card {
            width: 100% !important;
            min-width: 0 !important;
            padding: 1.2rem !important;
        }

        .bg-card-prob {
            font-size: 2.55rem !important;
        }

        .bg-section-header {
            margin-top: 1.8rem !important;
            font-size: 1.12rem !important;
        }

        div[data-testid="stLinkButton"] {
            width: 100% !important;
        }

        div[data-testid="stLinkButton"] a {
            width: 100% !important;
            justify-content: center !important;
        }

        .bg-footer {
            font-size: 0.76rem !important;
        }
    }


    @media (max-width: 390px) {

        .bg-hero-label {
            font-size: 2.05rem !important;
        }

        .bg-card-prob {
            font-size: 2.3rem !important;
        }

        .bg-card-threshold {
            font-size: 0.8rem !important;
        }
    }

</style>
"""
)


# ============================================================
# CONSTANTS
# ============================================================

OFFICIAL_URL = "https://www.smchealth.org/beaches"

SITE_LAT = 37.5602
SITE_LON = -122.2910


# ============================================================
# LOAD PREDICTION
# ============================================================

live_prediction = True
live_error = None

try:

    latest = load_live_latest()

except Exception as exc:

    live_prediction = False
    live_error = exc

    try:

        latest = load_latest()

    except Exception:

        st.error(
            "AquaCast cannot retrieve the latest forecast right now. "
            "Please check the official San Mateo County advisory."
        )

        st.link_button(
            "Check Official Water-Quality Advisories",
            OFFICIAL_URL,
            type="primary",
            use_container_width=True,
        )

        st.stop()


# ============================================================
# NORMALIZE DATES
# ============================================================

prediction_date = pd.to_datetime(
    latest["prediction_date"],
    errors="coerce",
)

updated_date = pd.to_datetime(
    latest["data_last_updated"],
    errors="coerce",
)


# ============================================================
# HERO
# ============================================================

render_hero(latest)


# ============================================================
# PRIMARY ACTION
# ============================================================

button_left, button_center, button_right = st.columns(
    [2.5, 5, 2.5]
)

with button_center:

    st.link_button(
        "Check Official Water-Quality Advisories",
        OFFICIAL_URL,
        type="primary",
        use_container_width=True,
    )


# ============================================================
# MAIN VALUES
# ============================================================

updated_str = (
    updated_date.strftime("%b %d, %Y")
    if pd.notna(updated_date)
    else "Unknown"
)

model_ver = str(
    latest["model_version"]
).upper()


ecoli_risk = str(
    latest["e_coli_risk"]
).strip()

ecoli_prob = float(
    latest["e_coli_probability"]
)

ecoli_cls = {
    "Safe": "safe",
    "Caution": "caution",
    "Unsafe": "unsafe",
}.get(
    ecoli_risk,
    "safe",
)


entero_risk = str(
    latest["enterococcus_risk"]
).strip()

entero_prob = float(
    latest["enterococcus_probability"]
)

entero_cls = {
    "Safe": "safe",
    "Caution": "caution",
    "Unsafe": "unsafe",
}.get(
    entero_risk,
    "safe",
)


# ============================================================
# FRESHNESS CHIP
# ============================================================

freshness_html = ""

if pd.notna(updated_date):

    days_old = (
        pd.Timestamp(date.today())
        - updated_date.normalize()
    ).days

    if days_old <= 0:

        freshness_html = (
            '<div class="bg-freshness current">'
            'Updated today'
            '</div>'
        )

    elif days_old == 1:

        freshness_html = (
            '<div class="bg-freshness current">'
            'Updated yesterday'
            '</div>'
        )

    elif days_old <= 3:

        freshness_html = (
            f'<div class="bg-freshness warn">'
            f'Updated {days_old} days ago'
            f'</div>'
        )

    else:

        freshness_html = (
            f'<div class="bg-freshness error">'
            f'Outdated · Last updated '
            f'{updated_date.strftime("%b %d, %Y")}'
            f'</div>'
        )


# ============================================================
# FORECAST METADATA + BACTERIA CARDS
# ============================================================

prediction_date_text = (
    prediction_date.strftime("%b %d, %Y")
    if pd.notna(prediction_date)
    else "Unknown"
)


st.html(
    f"""
<div class="bg-content">

    <div class="bg-stat-row">

        <div class="bg-stat">
            <p class="bg-stat-label">
                Forecast date
            </p>

            <p class="bg-stat-value">
                {prediction_date_text}
            </p>
        </div>


        <div class="bg-stat">
            <p class="bg-stat-label">
                Data freshness
            </p>

            <p class="bg-stat-value">
                {updated_str}
            </p>
        </div>

    </div>


    {freshness_html}


    <p class="bg-section-header">
        Water Quality Risk
    </p>


    <div class="bg-card-row">

        <div class="bg-card {ecoli_cls}">

            <p class="bg-card-name">
                E. coli
            </p>

            {badge(ecoli_risk)}

            <p class="bg-card-prob">
                {ecoli_prob:.0%}
            </p>

            <p class="bg-card-sublabel">
                Predicted exceedance probability
            </p>

            <p class="bg-card-threshold">
                Concentration threshold:
                235 MPN/100 mL
                <br>
                Safe &lt;10%
                &nbsp;·&nbsp;
                Caution 10–50%
                &nbsp;·&nbsp;
                Unsafe ≥50%
            </p>

        </div>


        <div class="bg-card {entero_cls}">

            <p class="bg-card-name">
                Enterococcus
            </p>

            {badge(entero_risk)}

            <p class="bg-card-prob">
                {entero_prob:.0%}
            </p>

            <p class="bg-card-sublabel">
                Predicted exceedance probability
            </p>

            <p class="bg-card-threshold">
                Concentration threshold:
                130 MPN/100 mL
                <br>
                Safe &lt;40%
                &nbsp;·&nbsp;
                Caution 40–85%
                &nbsp;·&nbsp;
                Unsafe ≥85%
            </p>

        </div>

    </div>


    <p class="bg-section-header">
        Pilot Site
    </p>

</div>
"""
)


# ============================================================
# MAP
# ============================================================

col_l, col_c, col_r = st.columns(
    [1.5, 9, 1.5]
)

with col_c:

    with st.container(
        border=True
    ):

        st.html(
            """
<p class="bg-map-title">
    Parkside Aquatic Park
</p>

<p class="bg-map-subtitle">
    San Mateo, California · AquaCast pilot monitoring site
</p>
"""
        )

        map_data = pd.DataFrame(
            {
                "lat": [
                    SITE_LAT
                ],

                "lon": [
                    SITE_LON
                ],
            }
        )

        st.map(
            map_data,
            zoom=14,
        )


# ============================================================
# MAP LABEL + FOOTER
# ============================================================

live_status = (
    "Live weather-based forecast"
    if live_prediction
    else "Latest saved forecast"
)


st.html(
    f"""
<div class="bg-content">

    <p class="bg-map-label">

        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="13"
            height="13"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#667085"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <path
                d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"
            />

            <circle
                cx="12"
                cy="10"
                r="3"
            />
        </svg>

        Parkside Aquatic Park, San Mateo, California
        &nbsp;·&nbsp;
        {live_status}

    </p>


    <div class="bg-footer">

        <strong>
            BeachGuard / AquaCast
        </strong>

        &nbsp;·&nbsp;

        Experimental research prototype

        &nbsp;·&nbsp;

        Model {model_ver}

        &nbsp;·&nbsp;

        <a
            href="{OFFICIAL_URL}"
            target="_blank"
        >
            Official Advisories
        </a>

    </div>

</div>
"""
)
