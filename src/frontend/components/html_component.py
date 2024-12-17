from dataclasses import dataclass

from espn_api.basketball import Team
from jinja2 import Template


@dataclass
class MatchupInput:
    home_team: Team
    away_team: Team
    home_team_score: int
    away_team_score: int
    ties: int
    matchup_scores: list[dict[str, int]]


def get_matchup_html(data: MatchupInput):
    with open("src/frontend/components/matchup.html", "r") as f:
        template = Template(f.read())

    return template.render(
        home_logo=data.home_team.logo_url,
        away_logo=data.away_team.logo_url,
        home_team=data.home_team.team_name,
        away_team=data.away_team.team_name,
        wins=data.home_team_score,
        losses=data.away_team_score,
        ties=data.ties,
        matchup_scores=data.matchup_scores,
    )


def get_team_viewer_html(data):
    with open("src/frontend/components/team_viewer.html", "r") as f:
        template = Template(f.read())

    return template.render(metrics=data)
