import streamlit as st
import streamlit.components.v1 as components
from espn_api.basketball.box_score import H2HCategoryBoxScore

import src.backend as be
import src.constants as const
import src.frontend.components.html_component as html
from src.frontend.streamlit_utils import page_setup

page_setup()

league_data = st.session_state.league_data
teams = st.session_state.teams
league_df = st.session_state.league_df

st.title(f"Week {league_data.currentMatchupPeriod} - Matchup Viewer")
st.markdown("Select a matchup in the sidebar to view the head-to-head category breakdown.")
box_scores: list[H2HCategoryBoxScore] = be.get_league_box_scores(league_data)
box_scores_formatted = [
    f"{match.home_team.team_name} vs {match.away_team.team_name}" for match in box_scores
]


selected_match = st.sidebar.radio("Matches", box_scores_formatted)
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

st.info("These are updated once a day in early morning.")
matchup_input = html.MatchupInput(
    box_score.home_team,
    box_score.away_team,
    box_score.home_wins,
    box_score.away_wins,
    box_score.home_ties,
    matchup_scores=agg_cat_scores,
)
components.html(html.get_matchup_html(matchup_input), height=425)
