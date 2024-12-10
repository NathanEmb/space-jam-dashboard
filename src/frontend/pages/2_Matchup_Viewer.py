import streamlit as st

import src.backend as be

# App configuration
icon_url = "https://spacejam-dashboard.s3.us-east-2.amazonaws.com/assets/the-last-spacejam.jpg"
st.set_page_config(layout="wide", page_title="Spacejam Dashboard", page_icon=icon_url)
st.logo(icon_url, size="large")


# Cached data behind it all
@st.cache_data
def update_league_data():
    return be.get_league()


league_data = update_league_data()
if "league_data" not in st.session_state:
    st.session_state.league_data = league_data
league_df = be.get_league_cat_data_rankings(league_data)
if "league_df" not in st.session_state:
    st.session_state.league_df = league_df
teams = [team.team_name for team in league_data.teams.values()]
if "teams" not in st.session_state:
    st.session_state.teams = teams


st.title("Coming soon....🚧")

st.header("And now, a joke powered by AI 🤖")
st.write(be.get_mainpage_joke())
