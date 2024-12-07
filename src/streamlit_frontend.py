import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

import src.backend as be
import src.constants as const

ryg = plt.colormaps["RdYlGn"]
gyr = plt.colormaps["RdYlGn"].reversed()
icon_url = "https://spacejam-dashboard.s3.us-east-2.amazonaws.com/assets/the-last-spacejam.jpg"
st.set_page_config(layout="wide", page_title="Spacejam Dashboard", page_icon=icon_url)
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
st.sidebar.markdown("# About")
st.sidebar.markdown("Welcome to the Space Jam Dashboard!")
st.sidebar.markdown(
    "This is my attempt at democratizing data and having fun coding. Let me know what you think (as long as it is good if you think it sucks I hate you.)"
)
page = st.sidebar.radio(
    "Select a Page", ("League Overview", "Team Overview")
)  # , "Matchup Overview"))

# League Overview Page
if page == "League Overview":
    league_df = be.get_league_cat_data_rankings(league_data)
    league_df_styled = league_df.style.background_gradient(cmap=gyr)
    st.title("Spacejam League Overview")
    st.dataframe(league_df_styled, use_container_width=True, hide_index=True, height=460)
    st.markdown(
        "As you can imagine, green means that this team is good in that category, and red means the team is bad in that category."
    )

# Team Overview Page
elif page == "Team Overview":
    chosen_team = st.sidebar.selectbox("Team", teams)
    team_data = league_data.teams[chosen_team]
    st.title(f"Overview - {chosen_team}")
    st.write("Stats for", chosen_team)
    timeframe = st.radio(label="Time:", options=["30 Days", "15 Days", "7 Days"], horizontal=True)
    timeframe_num = int(timeframe.split(" ")[0])
    team_avg_stats = be.get_average_team_stats(team_data, timeframe_num)
    df = pd.DataFrame(team_avg_stats).T.fillna(0)
    show_cols = st.multiselect("Column Filter", options=df.columns, default=const.NINE_CATS)
    st.dataframe(df[show_cols], use_container_width=True, height=460)

# Matchup Overview Page
elif page == "Matchup Overview":
    st.title(f"Matchup Overview - {chosen_team}")
    st.write("Matchup Stats for", chosen_team)
    st.table(matchup_df.loc[matchup_df["Team"] == chosen_team])
