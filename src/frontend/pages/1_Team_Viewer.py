import streamlit as st
from espn_api.basketball import Team

import src.backend as be
import src.constants as const
import src.frontend.figures as fig
from src.frontend.components.html_component import get_team_viewer_html
from src.frontend.streamlit_utils import page_setup

page_setup()


league_data = st.session_state.league_data
teams = st.session_state.teams
league_df = st.session_state.league_df

chosen_team = st.sidebar.radio("Team", teams)
st.title(chosen_team)
team_data = league_data.team_dict[chosen_team]
seven_day_stats = be.get_average_team_stats(team_data, 7)
fifteen_day_stats = be.get_average_team_stats(team_data, 15)
thirty_day_stats = be.get_average_team_stats(team_data, 30)
agg_stats = be.agg_player_avgs(seven_day_stats, fifteen_day_stats, thirty_day_stats)
team_obj: Team = league_data.team_dict[chosen_team]
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
team_data = league_df.loc[league_df["Team"] == chosen_team].to_dict("records")[0]
strengths, weaknesses, punts = be.get_team_breakdown(team_data)

st.subheader("Team Strengths")
st.markdown("Team ranks in top 4 of these categories.")
st.html(get_team_viewer_html(strengths))

st.subheader("Could go either way")
st.markdown("Team ranks in middle 4 of these categories.")
st.html(get_team_viewer_html(weaknesses))

st.subheader("Team Punts")
st.markdown("Team ranks in bottom 4 of league in these categories. (hopefully on purpose)")
st.html(get_team_viewer_html(punts))

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
