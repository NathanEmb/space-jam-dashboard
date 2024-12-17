import streamlit as st
from streamlit_autorefresh import st_autorefresh

import src.backend as be


def create_metric_grid(data: dict[str, float], num_cats_per_row: int = 3):
    j = 0
    rows_of_cols = []
    while data:
        rows_of_cols.append(st.columns(num_cats_per_row))
        for i in range(num_cats_per_row):
            try:
                cat = list(data.keys())[0]
            except IndexError:
                break
            val = data.pop(cat)
            rows_of_cols[j][i].metric(cat, val)
        j += 1


def page_setup(title="Space Jammers Lounge"):
    # App configuration
    icon_url = "https://spacejam-dashboard.s3.us-east-2.amazonaws.com/assets/the-last-spacejam.jpg"
    st.set_page_config(
        page_title=title,
        page_icon=icon_url,
        menu_items={
            "Report a bug": "https://github.com/NathanEmb/space-jam-dashboard/issues",
            "About": "https://github.com/NathanEmb/space-jam-dashboard",
        },
        layout="wide",
    )

    st.logo(icon_url, size="large")
    refresh_in_sec = 600
    st_autorefresh(interval=refresh_in_sec * 1000, limit=100, key="statscounter")

    # Cached data behind it all
    @st.cache_data
    def update_league_data():
        return be.get_league()

    if "league_data" not in st.session_state:
        league_data = update_league_data()
        st.session_state.league_data = league_data
    if "league_df" not in st.session_state:
        league_df = be.get_league_cat_data_rankings(league_data)
        st.session_state.league_df = league_df
    if "teams" not in st.session_state:
        teams = [team.team_name for team in league_data.teams]
        st.session_state.teams = teams
