import streamlit as st
import streamlit.components.v1 as components
from espn_api.basketball.box_score import H2HCategoryBoxScore

import src.backend as be
import src.constants as const
import src.frontend.components.html_component as html

# App configuration
icon_url = "https://spacejam-dashboard.s3.us-east-2.amazonaws.com/assets/the-last-spacejam.jpg"
st.set_page_config(layout="wide", page_title="Matchup Viewer", page_icon=icon_url)
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
st.markdown("Select a matchup in the sidebar to view the head-to-head category breakdown.")
box_scores: list[H2HCategoryBoxScore] = be.get_league_box_scores(league_data)
box_scores_formatted = [
    f"{match.home_team.team_name} vs {match.away_team.team_name}" for match in box_scores
]


selected_match = st.sidebar.selectbox("Matches", box_scores_formatted)
match_index = box_scores_formatted.index(selected_match)

box_score = box_scores[match_index]

agg_cat_scores = []
for cat, data in box_score.home_stats.items():
    if cat in const.NINE_CATS:
        agg_cat_scores.append(
            {
                "name": cat,
                "home": round(data["value"], 2),
                "away": round(box_score.away_stats[cat]["value"], 2),
            }
        )

matchup_input = html.MatchupInput(
    box_score.home_team,
    box_score.away_team,
    box_score.home_wins,
    box_score.away_wins,
    box_score.home_ties,
    matchup_scores=agg_cat_scores,
)
components.html(html.get_matchup_html(matchup_input), height=5000)

st.markdown(
    "This is basically just ESPN viewer right now...I get that. I'd like to add actual vs projected for the week + some information surrounding available players and how they might impact your matchup...but it's a lot of work."
)
