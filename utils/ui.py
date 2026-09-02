import html
from datetime import date

import pandas as pd
import streamlit as st


OFFICIAL_URL = "https://www.smchealth.org/beaches"
GITHUB_URL = "https://github.com/XL-DSL/Aquacast-Beachgaurd"

SITE_NAME = "Parkside Aquatic Park, San Mateo"


def risk_class(risk):
    return {
        "Safe": "safe",
        "Caution": "caution",
        "Unsafe": "unsafe",
    }.get(str(risk).strip(), "safe")


def risk_icon(risk):
    return {
        "Safe": "✓",
        "Caution": "!",
        "Unsafe": "×",
    }.get(str(risk).strip(), "•")


def interpretation(risk):
    return {
        "Safe": (
            "The model currently predicts a low likelihood "
            "of elevated bacterial risk."
        ),
        "Caution": (
            "The model predicts moderate or uncertain risk. "
            "Check official advisories before entering the water."
        ),
        "Unsafe": (
            "The model predicts elevated bacterial risk. "
            "Avoid water contact and follow official advisories."
        ),
    }.get(
        str(risk).strip(),
        "Current model risk is unavailable.",
    )


def freshness_chip(updated_date):
    updated = pd.to_datetime(
        updated_date,
        errors="coerce",
    )

    if pd.isna(updated):
        return (
            '<span class="bg-fresh-chip stale">'
            'Update time unavailable'
            '</span>'
        )

    if updated.tzinfo is not None:
        updated = updated.tz_localize(None)

    days_old = (
        pd.Timestamp(date.today())
        - updated.normalize()
    ).days

    if days_old <= 0:
        text = "Updated today"
        css_class = "current"

    elif days_old == 1:
        text = "Updated yesterday"
        css_class = "current"

    elif days_old <= 7:
        text = f"Updated {days_old} days ago"
        css_class = "warn"

    else:
        text = (
            "Outdated · Last updated "
            + updated.strftime("%b %d, %Y")
        )
        css_class = "stale"

    return (
        f'<span class="bg-fresh-chip {css_class}">'
        f'{text}'
        f'</span>'
    )


def probability_meter(
    probability,
    caution_threshold,
    unsafe_threshold,
    risk,
):
    probability = max(
        0.0,
        min(
            float(probability),
            1.0,
        ),
    )

    value = probability * 100
    caution = caution_threshold * 100
    unsafe = unsafe_threshold * 100
    css_class = risk_class(risk)

    return f"""
<div
    class="bg-meter"
    role="img"
    aria-label="Predicted exceedance probability {value:.0f} percent.
    Caution threshold {caution:.0f} percent.
    Unsafe threshold {unsafe:.0f} percent."
>

    <div class="bg-meter-track">

        <div
            class="bg-meter-marker caution-marker"
            style="left:{caution:.0f}%"
        ></div>

        <div
            class="bg-meter-marker unsafe-marker"
            style="left:{unsafe:.0f}%"
        ></div>

        <div
            class="bg-meter-pointer {css_class}"
            style="left:{value:.1f}%"
        ></div>

    </div>

    <div class="bg-meter-labels">

        <span>0%</span>

        <span
            class="bg-meter-boundary"
            style="left:{caution:.0f}%"
        >
            Caution {caution:.0f}%
        </span>

        <span
            class="bg-meter-boundary"
            style="left:{unsafe:.0f}%"
        >
            Unsafe {unsafe:.0f}%
        </span>

        <span>100%</span>

    </div>

</div>
"""


def render_footer(model_version=None):
    version_html = ""

    if model_version:
        version_html = (
            " &nbsp;·&nbsp; "
            f'<span>{html.escape(str(model_version))}</span>'
        )

    st.html(
        f"""
<div class="bg-site-footer">

    <div>
        <strong>BeachGuard / AquaCast</strong>
        &nbsp;·&nbsp;
        Experimental research prototype
        {version_html}
    </div>

    <div class="bg-footer-links">

        <a
            href="{OFFICIAL_URL}"
            target="_blank"
        >
            Official Advisories
        </a>

        <a
            href="{GITHUB_URL}"
            target="_blank"
        >
            GitHub
        </a>

        <span>
            Methodology available in About AquaCast
        </span>

    </div>

</div>
"""
    )
