import matplotlib.pyplot as plt
import streamlit as st
from espn_api.basketball import Team
from streamlit_autorefresh import st_autorefresh

import src.backend as be
import src.constants as const
import src.figures as fig
import src.streamlit_utils as su

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
chosen_team = st.sidebar.selectbox("Team", teams)
page = st.sidebar.radio(
    "Select a Page", ("League Overview", "Team Overview")
)  # , "Matchup Overview"))

league_df = be.get_league_cat_data_rankings(league_data)

# League Overview Page
if page == "League Overview":
    league_df_styled = league_df.style.background_gradient(cmap=gyr)
    st.title("Spacejam League Overview")
    st.dataframe(league_df_styled, use_container_width=True, hide_index=True, height=460)
    st.markdown(
        "As you can imagine, green means that this team is good in that category, and red means the team is bad in that category."
    )
# Team Overview Page
elif page == "Team Overview":
    st.title(f"Overview - {chosen_team}")
    team_obj: Team = league_data.teams[chosen_team]
    st.write(team_obj.wins, team_obj.losses, team_obj.ties)
    st.header("Category Rankings")
    left_col, mid_col, right_col = st.columns(3)
    team_data = league_df.loc[league_df["Team"] == chosen_team].to_dict("records")[0]
    strengths, weaknesses, punts = be.get_team_breakdown(team_data)

    num_cats_per_row = 2
    with left_col:
        st.subheader("Team Strengths")
        su.create_metric_grid(strengths, num_cats_per_row)

    with mid_col:
        st.subheader("Could go either way")
        su.create_metric_grid(weaknesses, num_cats_per_row)

    with right_col:
        st.subheader("Team Punts")
        su.create_metric_grid(punts, num_cats_per_row)

    team_data = league_data.teams[chosen_team]

    with st.expander("📊 Team Trends"):
        st.write("Team Trends - ", chosen_team)
        seven_day_stats = be.get_average_team_stats(team_data, 7)
        fifteen_day_stats = be.get_average_team_stats(team_data, 15)
        thirty_day_stats = be.get_average_team_stats(team_data, 30)
        agg_stats = be.agg_player_avgs(seven_day_stats, fifteen_day_stats, thirty_day_stats)
        fig = fig.create_cat_bar_charts(agg_stats.T)
        st.pyplot(fig)

    with st.expander("🏀 Player Stats"):
        timeframe = st.radio("Past:", ["7 Days", "15 Days", "30 Days"], horizontal=True)
        show_cols = st.multiselect(
            "Column Filter", options=seven_day_stats.columns, default=const.NINE_CATS
        )
        if timeframe == "7 Days":
            st.dataframe(seven_day_stats[show_cols], use_container_width=True)
        elif timeframe == "15 Days":
            st.dataframe(fifteen_day_stats[show_cols], use_container_width=True)
        elif timeframe == "30 Days":
            st.dataframe(thirty_day_stats[show_cols], use_container_width=True)

# Matchup Overview Page
elif page == "Matchup Overview":
    st.title(f"Matchup Overview - {chosen_team}")
    st.write("Matchup Stats for", chosen_team)
    st.table(matchup_df.loc[matchup_df["Team"] == chosen_team])
