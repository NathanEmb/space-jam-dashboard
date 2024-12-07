import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

import src.backend as be

ryg = plt.colormaps["RdYlGn"]
gyr = plt.colormaps["RdYlGn"].reversed()

st.set_page_config(layout="wide")
refresh_in_sec = 60
count = st_autorefresh(interval=refresh_in_sec * 1000, limit=100, key="statscounter")


@st.cache_data
def update_league_data():
    return be.get_league()


league_data = update_league_data()

teams = [team.team_name for team in league_data.teams.values()]


matchup_df = be.get_league_cat_raw_stats_df(league_data)
team_stats_df = be.get_league_all_raw_data_rankings(league_data)


# Sidebar for page selection
st.sidebar.title("Navigation")
chosen_team = st.sidebar.selectbox("Team", teams)
page = st.sidebar.radio("Select a Page", ("League Overview", "Team Overview", "Matchup Overview"))

# League Overview Page
if page == "League Overview":
    league_df = be.get_league_cat_data_rankings(league_data)
    league_df_styled = league_df.style.background_gradient(cmap=gyr)
    st.title("Spacejam League Overview")
    st.dataframe(league_df_styled, use_container_width=True, hide_index=True, height=460)

# Team Overview Page
elif page == "Team Overview":
    team_data = league_data.teams[chosen_team]
    st.title(f"Overview - {chosen_team}")
    st.write("Stats for", chosen_team)
    timeframe = st.radio(label="Time:", options=["30 Days", "15 Days", "7 Days"], horizontal=True)
    timeframe_num = int(timeframe.split(" ")[0])
    team_avg_stats = be.get_average_team_stats(team_data, timeframe_num)
    st.table(pd.DataFrame(team_avg_stats).T.fillna(0))

# Matchup Overview Page
elif page == "Matchup Overview":
    st.title(f"Matchup Overview - {chosen_team}")
    st.write("Matchup Stats for", chosen_team)
    st.table(matchup_df.loc[matchup_df["Team"] == chosen_team])
