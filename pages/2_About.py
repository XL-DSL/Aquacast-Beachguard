import streamlit as st

from utils.styles import apply_styles
from utils.ui import render_footer


st.set_page_config(
    page_title="About AquaCast | BeachGuard",
    page_icon="🌊",
    layout="wide",
)

apply_styles()


st.html(
    """
<div class="bg-reading">

    <div class="bg-page-heading">

        <h1>
            About AquaCast
        </h1>

        <p>
            How environmental information becomes
            a BeachGuard water-quality risk forecast.
        </p>

    </div>


    <h2 class="bg-reading-heading">
        How AquaCast Works
    </h2>


    <div class="bg-workflow">

        <div class="bg-workflow-card">

            <div class="bg-workflow-number">
                1
            </div>

            <strong>
                Environmental Data
            </strong>

            <span>
                Rainfall, temperature,
                recent weather patterns,
                and historical bacterial monitoring.
            </span>

        </div>


        <div class="bg-workflow-arrow">
            →
        </div>


        <div class="bg-workflow-card">

            <div class="bg-workflow-number">
                2
            </div>

            <strong>
                AquaCast Model
            </strong>

            <span>
                Machine-learning models evaluate
                environmental conditions associated
                with bacterial exceedances.
            </span>

        </div>


        <div class="bg-workflow-arrow">
            →
        </div>


        <div class="bg-workflow-card">

            <div class="bg-workflow-number">
                3
            </div>

            <strong>
                Risk Forecast
            </strong>

            <span>
                BeachGuard converts model probabilities
                into Safe, Caution, or Unsafe
                decision-support categories.
            </span>

        </div>

    </div>


    <section class="bg-reading-section">

        <h2>
            What AquaCast Predicts
        </h2>

        <p>
            AquaCast estimates the probability that
            E. coli or Enterococcus will exceed an
            elevated-risk concentration threshold at
            Parkside Aquatic Park, San Mateo.
        </p>

        <p>
            AquaCast performs classification rather than
            attempting to predict an exact bacterial
            concentration. Laboratory sampling is still
            required to directly measure bacteria levels.
        </p>

    </section>


    <section class="bg-reading-section">

        <h2>
            Model Development
        </h2>

        <p>
            AquaCast was developed using historical
            recreational-water monitoring and environmental
            data. The model pipeline uses chronological
            training, validation, and test periods so that
            earlier observations are used to predict later
            conditions rather than randomly mixing past
            and future data.
        </p>

        <p>
            Current live forecasts extend the research
            prototype by incorporating recent and forecast
            weather while retaining the existing AquaCast
            model structure.
        </p>

    </section>


    <h2 class="bg-reading-heading">
        Data Sources
    </h2>


    <div class="bg-source-grid">

        <a
            class="bg-source-card"
            href="https://www.waterboards.ca.gov/"
            target="_blank"
        >

            <span class="bg-source-label">
                Monitoring Data
            </span>

            <strong>
                California Water Boards
            </strong>

            <p>
                Historical fecal-indicator bacteria
                monitoring records.
            </p>

        </a>


        <a
            class="bg-source-card"
            href="https://www.ncei.noaa.gov/"
            target="_blank"
        >

            <span class="bg-source-label">
                Historical Weather
            </span>

            <strong>
                NOAA / NCEI
            </strong>

            <p>
                Historical precipitation and
                temperature observations.
            </p>

        </a>


        <a
            class="bg-source-card"
            href="https://open-meteo.com/"
            target="_blank"
        >

            <span class="bg-source-label">
                Live Forecast Weather
            </span>

            <strong>
                Open-Meteo
            </strong>

            <p>
                Recent and forecast environmental
                conditions used by the live support layer.
            </p>

        </a>

    </div>


    <section class="bg-reading-section">

        <h2>
            Why E. coli and Enterococcus?
        </h2>

        <p>
            E. coli and Enterococcus are fecal-indicator
            bacteria commonly used to evaluate recreational
            water quality. Elevated indicator levels can
            be associated with increased risk of illness
            from water contact.
        </p>

    </section>


    <section class="bg-reading-section">

        <h2>
            Development Transparency
        </h2>

        <p>
            AI-assisted tools were used for limited
            code support, debugging, review, and
            documentation. The project developer remains
            responsible for understanding, testing,
            editing, and maintaining the submitted code.
        </p>

    </section>

</div>
"""
)


render_footer()
