"""FastAPI application for Space Jammers Dashboard."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from pathlib import Path

import src.backend as be
import src.constants as const
from src.frontend.figures import create_cat_bar_charts

app = FastAPI(title="Space Jammers Dashboard")

# Setup templates
templates = Jinja2Templates(directory="src/frontend/templates")

# Global data cache - loaded once at startup
league_data = None
league_df = None
teams = None


@app.on_event("startup")
async def startup_event():
    """Load league data on startup."""
    global league_data, league_df, teams
    league_data = be.get_league()
    league_df = be.get_league_cat_data_rankings(league_data)
    teams = [team.team_name for team in league_data.teams]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main dashboard page with category rankings."""
    # Get AI joke
    try:
        joke = be.get_mainpage_joke()
    except Exception:
        joke = "The bots broke.."

    # Prepare league data for template
    league_df_dict = league_df.to_dict('records')
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "joke": joke,
            "league_data": league_df_dict,
            "columns": list(const.CAT_ONLY_DATA_RANKED_TABLE_DEF.keys())
        }
    )


@app.get("/team/{team_name}", response_class=HTMLResponse)
async def team_viewer(request: Request, team_name: str):
    """Team viewer page showing detailed team statistics."""
    team_obj = league_data.team_dict[team_name]
    
    # Get player stats for different timeframes
    seven_day_stats = be.get_average_team_stats(team_obj, 7)
    fifteen_day_stats = be.get_average_team_stats(team_obj, 15)
    thirty_day_stats = be.get_average_team_stats(team_obj, 30)
    agg_stats = be.agg_player_avgs(seven_day_stats, fifteen_day_stats, thirty_day_stats)
    
    # Get team breakdown
    team_data = league_df.loc[league_df["Team"] == team_name].to_dict("records")[0]
    strengths, weaknesses, punts = be.get_team_breakdown(team_data)
    
    # Generate chart
    fig = create_cat_bar_charts(agg_stats.T)
    
    # Convert figure to base64 encoded image
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    chart_img = base64.b64encode(img_buffer.read()).decode()
    plt.close(fig)
    
    # Get AI joke about team
    try:
        team_joke = be.get_teamviewer_joke(team_name)
    except Exception:
        team_joke = "The bots broke.."
    
    return templates.TemplateResponse(
        "team.html",
        {
            "request": request,
            "team_name": team_name,
            "team": team_obj,
            "standing": team_obj.standing,
            "division": team_obj.division_name,
            "wins": team_obj.wins,
            "losses": team_obj.losses,
            "ties": team_obj.ties,
            "acquisitions": team_obj.acquisitions,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "punts": punts,
            "chart_img": chart_img,
            "seven_day_stats": seven_day_stats.to_dict('index'),
            "fifteen_day_stats": fifteen_day_stats.to_dict('index'),
            "thirty_day_stats": thirty_day_stats.to_dict('index'),
            "nine_cats": const.NINE_CATS,
            "all_columns": list(seven_day_stats.columns),
            "teams": teams,
            "team_joke": team_joke
        }
    )


@app.get("/matchup/{matchup_index}", response_class=HTMLResponse)
async def matchup_viewer(request: Request, matchup_index: int = 0):
    """Matchup viewer page showing head-to-head comparisons."""
    box_scores = be.get_league_box_scores(league_data)
    
    # Get selected matchup
    box_score = box_scores[matchup_index]
    
    # Aggregate category scores
    agg_cat_scores = []
    for cat, data in box_score.home_stats.items():
        if cat in const.NINE_CATS:
            agg_cat_scores.append({
                "name": cat,
                "home": round(data["value"], 2),
                "away": round(box_score.away_stats[cat]["value"], 2),
            })
    
    # Format matchups for selector
    matchups = [
        {
            "index": i,
            "label": f"{match.home_team.team_name} vs {match.away_team.team_name}"
        }
        for i, match in enumerate(box_scores)
    ]
    
    return templates.TemplateResponse(
        "matchup.html",
        {
            "request": request,
            "home_team": box_score.home_team,
            "away_team": box_score.away_team,
            "home_wins": box_score.home_wins,
            "away_wins": box_score.away_wins,
            "ties": box_score.home_ties,
            "matchup_scores": agg_cat_scores,
            "matchups": matchups,
            "selected_index": matchup_index,
            "current_week": league_data.currentMatchupPeriod,
            "teams": teams
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5006)
