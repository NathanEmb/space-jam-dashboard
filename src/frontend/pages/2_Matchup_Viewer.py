import streamlit as st
from espn_api.basketball.box_score import H2HCategoryBoxScore

import src.backend as be

# App configuration
icon_url = "https://spacejam-dashboard.s3.us-east-2.amazonaws.com/assets/the-last-spacejam.jpg"
st.set_page_config(layout="centered", page_title="Matchup Viewer", page_icon=icon_url)
st.logo(icon_url, size="large")


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
    teams = [team.team_name for team in league_data.team_dict.values()]
    st.session_state.teams = teams

league_data = st.session_state.league_data
teams = st.session_state.teams
league_df = st.session_state.league_df

st.title(f"Week {league_data.currentMatchupPeriod} - Matchup Viewer")
box_scores: list[H2HCategoryBoxScore] = be.get_league_box_scores(league_data)
box_scores_formatted = [
    f"{match.home_team.team_name} vs {match.away_team.team_name}" for match in box_scores
]
selected_match = st.selectbox("Matches", box_scores_formatted)
match_index = box_scores_formatted.index(selected_match)

home_team, scores, away_team = st.columns(3)
box_score = box_scores[match_index]

with home_team:
    st.header(f"**{box_score.home_team.team_name}** - {box_score.home_team.team_abbrev}")
    st.markdown(
        f"W-T-L: ({box_score.home_team.wins}-{box_score.home_team.ties}-{box_score.home_team.losses})"
    )
with scores:
    st.text("")
    st.text("")
    st.text("")

    st.header(f"{box_score.home_wins} - {box_score.home_ties} - {box_score.away_wins}")
with away_team:
    st.header(f"**{box_score.away_team.team_name}** - {box_score.away_team.team_abbrev}")
    st.markdown(
        f"W-T-L: ({box_score.away_team.wins}-{box_score.away_team.ties}-{box_score.away_team.losses})"
    )

st.header("H2H Scores", divider=True)
st.dataframe(be.get_matchup_score_df(league_data.scoreboard()[match_index]))
