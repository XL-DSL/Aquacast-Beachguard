import streamlit as st


# ==========================================================
# APP CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="BeachGuard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# PAGE DEFINITIONS
# ==========================================================

current_forecast = st.Page(
    "pages/0_Current_Forecast.py",
    title="Current Forecast",
    default=True,
)

timeline = st.Page(
    "pages/8_Timeline.py",
    title="Timeline",
)

recent_trends = st.Page(
    "pages/4_Recent_Trends.py",
    title="Recent Trends",
)

map_page = st.Page(
    "pages/5_Map.py",
    title="Map",
)

risk_details = st.Page(
    "pages/1_Risk_Details.py",
    title="Risk Details",
)

about = st.Page(
    "pages/2_About.py",
    title="About AquaCast",
)

safety = st.Page(
    "pages/3_Disclaimer.py",
    title="Safety & Data Notes",
)

limitations = st.Page(
    "pages/7_Limitations.py",
    title="Limitations",
)

model_data = st.Page(
    "pages/6_Model_and_Data.py",
    title="Model & Data",
)


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

navigation = st.navigation(
    {
        "🌊 BeachGuard": [
            current_forecast,
            timeline,
            recent_trends,
            map_page,
            risk_details,
        ],

        "About & Safety": [
            about,
            safety,
        ],

        "Technical": [
            limitations,
            model_data,
        ],
    },
    position="sidebar",
    expanded=True,
)


navigation.run()
