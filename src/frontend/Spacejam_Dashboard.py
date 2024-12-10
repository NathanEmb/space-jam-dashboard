import matplotlib.pyplot as plt
import streamlit as st
from espn_api.basketball import Team
from streamlit_autorefresh import st_autorefresh

import src.backend as be
import src.constants as const
import src.frontend.figures as fig
import src.frontend.streamlit_utils as su

icon_url = "https://spacejam-dashboard.s3.us-east-2.amazonaws.com/assets/the-last-spacejam.jpg"
st.set_page_config(layout="wide", page_title="Spacejam Dashboard", page_icon=icon_url)
refresh_in_sec = 600
count = st_autorefresh(interval=refresh_in_sec * 1000, limit=100, key="statscounter")

st.logo(icon_url, size="large")


@st.cache_data
def update_league_data():
    return be.get_league()


league_data = update_league_data()

teams = [team.team_name for team in league_data.teams.values()]


matchup_df = be.get_league_cat_raw_stats_df(league_data)
team_stats_df = be.get_league_all_raw_data_rankings(league_data)


# Sidebar for page selection
st.sidebar.header("Space Jam Dashboard")
page = st.sidebar.radio(
    "Navigation", (const.LEAGUE_OVERVIEW_TITLE, const.TEAM_PAGE_TITLE, const.MATCHUP_PAGE_TITLE)
)

league_df = be.get_league_cat_data_rankings(league_data)

# League Overview Page
if page == "League Overview":
    gyr = plt.colormaps["RdYlGn"].reversed()
    league_df_styled = league_df.style.background_gradient(cmap=gyr)
    st.title("Spacejam League Overview")
    st.dataframe(league_df_styled, use_container_width=True, hide_index=True, height=460)
    st.markdown(
        "As you can imagine, green means that this team is good in that category, and red means the team is bad in that category."
    )
# Team Overview Page
elif page == const.TEAM_PAGE_TITLE:
    st.title(const.TEAM_PAGE_TITLE)
    chosen_team = st.selectbox("Team", teams)
    team_data = league_data.teams[chosen_team]
    seven_day_stats = be.get_average_team_stats(team_data, 7)
    fifteen_day_stats = be.get_average_team_stats(team_data, 15)
    thirty_day_stats = be.get_average_team_stats(team_data, 30)
    agg_stats = be.agg_player_avgs(seven_day_stats, fifteen_day_stats, thirty_day_stats)
    team_obj: Team = league_data.teams[chosen_team]
    standing_col, record_col, acquisitions_col, div_col = st.columns(4, vertical_alignment="center")
    with standing_col:
        st.metric("League Wide Standing", f"{team_obj.standing}")
    with div_col:
        st.metric("Division:", f"{team_obj.division_name}")
    with record_col:
        st.metric("Current Record:", f"{team_obj.wins}W - {team_obj.losses}L - {team_obj.ties}T")
    with acquisitions_col:
        st.metric("Total Acquisitions Used:", f"{team_obj.acquisitions} / 70")

    st.header("Category Rankings")
    left_col, mid_col, right_col = st.columns(3)
    team_data = league_df.loc[league_df["Team"] == chosen_team].to_dict("records")[0]
    strengths, weaknesses, punts = be.get_team_breakdown(team_data)

    num_cats_per_row = 3
    with left_col:
        st.subheader("Team Strengths")
        st.markdown("Team ranks in top 4 of these categories.")
        su.create_metric_grid(strengths, num_cats_per_row)

    with mid_col:
        st.subheader("Could go either way")
        st.markdown("Team ranks in middle 4 of these categories.")
        su.create_metric_grid(weaknesses, num_cats_per_row)

    with right_col:
        st.subheader("Team Punts")
        st.markdown("Team ranks in bottom 4 of league in these categories. (hopefully on purpose)")
        su.create_metric_grid(punts, num_cats_per_row)

    with st.expander("🏀 Individual Player Stats"):
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

    with st.expander("📊 Team Category Trends"):
        st.write("Team Trends - ", chosen_team)
        fig = fig.create_cat_bar_charts(agg_stats.T)
        st.pyplot(fig)

# Matchup Overview Page
elif page == "Matchup Overview":
    st.title(f"Matchup Overview - {chosen_team}")
    st.write("Matchup Stats for", chosen_team)
    st.table(matchup_df.loc[matchup_df["Team"] == chosen_team])
