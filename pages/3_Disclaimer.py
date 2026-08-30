import streamlit as st

from utils.styles import apply_styles
from utils.ui import OFFICIAL_URL, render_footer


st.set_page_config(
    page_title="Safety & Data Notes | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


st.html(
    f"""
<div class="bg-reading">

    <div class="bg-page-heading">

        <h1>
            Safety & Data Notes
        </h1>

        <p>
            Important information about how to interpret
            BeachGuard forecasts.
        </p>

    </div>


    <div class="bg-safety-card">

        <div class="bg-safety-icon">
            !
        </div>

        <div>

            <h2>
                Experimental Forecast
            </h2>

            <p>
                BeachGuard / AquaCast is a research
                prototype. Its risk categories represent
                model-estimated probabilities and do not
                constitute an official determination that
                water is safe or unsafe for recreation.
            </p>

            <p>
                AquaCast does not directly measure current
                bacterial concentrations and should never
                replace laboratory results, official
                monitoring, beach closures, or public-health
                advisories.
            </p>

        </div>

    </div>


    <a
        class="bg-primary-button full-button"
        href="{OFFICIAL_URL}"
        target="_blank"
    >
        Check Official Water-Quality Advisories
    </a>


    <div class="bg-notes-grid">

        <div class="bg-notes-card">

            <h2>
                Forecast Inputs
            </h2>

            <p>
                Current forecasts use recent and forecast
                weather conditions together with the latest
                available historical monitoring information.
            </p>

            <p>
                Some previous-sample variables remain based
                on the latest valid laboratory observation
                until a newer result becomes available.
            </p>

        </div>


        <div class="bg-notes-card">

            <h2>
                Forecast Uncertainty
            </h2>

            <p>
                Weather forecasts, particularly rainfall
                forecasts, can be inaccurate. That
                uncertainty can affect the resulting
                AquaCast bacterial-risk estimate.
            </p>

            <p>
                Unusual contamination events or conditions
                outside the historical training range may
                also reduce model accuracy.
            </p>

        </div>

    </div>


    <div class="bg-data-source-summary">

        <h2>
            Data Sources
        </h2>

        <div class="bg-source-badges">

            <span>
                California Water Boards
            </span>

            <span>
                NOAA / NCEI
            </span>

            <span>
                Open-Meteo
            </span>

            <span>
                San Mateo County Advisories
            </span>

        </div>

    </div>


    <div class="bg-support-note">

        <strong>
            Official information always takes priority.
        </strong>

        Laboratory measurements, official advisories,
        beach closures, and agency notices should be used
        for final recreational-water decisions.

    </div>

</div>
"""
)


render_footer()
