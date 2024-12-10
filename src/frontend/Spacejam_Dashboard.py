import matplotlib.pyplot as plt
import streamlit as st
from streamlit_autorefresh import st_autorefresh

import src.backend as be

# App configuration
icon_url = "https://spacejam-dashboard.s3.us-east-2.amazonaws.com/assets/the-last-spacejam.jpg"
st.set_page_config(layout="wide", page_title="Spacejam Dashboard", page_icon=icon_url)
st.logo(icon_url, size="large")
refresh_in_sec = 600
count = st_autorefresh(interval=refresh_in_sec * 1000, limit=100, key="statscounter")


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

# Sidebar for page selection
st.sidebar.success("Welcome to the Spacejam Dashboard, written by the Tatums.")
st.sidebar.subheader("And now, a joke powered by AI 🤖")
st.sidebar.write(be.get_mainpage_joke())

# Main Page content
st.title("Spacejam Dashboard")
st.subheader("About")
st.markdown(
    "This dashboard serves two purposes: \n 1. Be a fun project for me to work on. \n 2. Provide some more data to everyone who isn't already paying for a fancy schmancy site already."
)
st.subheader("Category Rankings (Green is good)")
st.markdown(
    "This was the first bit of data that I wanted to understand when I was left with my head in my hands after a loss to Will saying 'What are the Tatum's good for?'"
)

gyr = plt.colormaps["RdYlGn"].reversed()
league_df_styled = league_df.style.background_gradient(cmap=gyr)
st.dataframe(league_df_styled, use_container_width=True, hide_index=True, height=460)
