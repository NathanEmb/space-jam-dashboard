import random
from copy import deepcopy

import pandas as pd
from espn_api.basketball import League, Matchup, Team
from groq import Groq

import src.constants as const
import src.prompts as prompts


def get_league(league_id: int = const.SPACEJAM_LEAGUE_ID, year: int = const.YEAR) -> League:
    """Get the league object for the specified league_id and year."""
    league = League(league_id, year)
    league.team_dict = {team.team_name: team for team in league.teams}
    return league


def get_league_all_raw_stats_df(league: League) -> pd.DataFrame:
    """Get every team's stats for all categories."""
    league_stats = []
    for team in league.team_dict.values():
        temp_dict = deepcopy(team.stats)
        temp_dict["Team"] = team.team_name
        temp_dict["Standing"] = team.standing
        league_stats.append(temp_dict)

    df = pd.DataFrame(league_stats)

    df = df.astype(const.ALL_RAW_DATA_TABLE_DEF)
    return df[list(const.ALL_RAW_DATA_TABLE_DEF.keys())].sort_values(by="Standing")


def get_league_all_raw_data_rankings(league: League) -> pd.DataFrame:
    """Get every team's ranking for all stats."""
    raw_stats_df = get_league_all_raw_stats_df(league)
    # Rank only numeric columns
    want_big_num_df = raw_stats_df[const.WANT_BIG_NUM]
    want_small_num_df = raw_stats_df[const.WANT_SMALL_NUM]
    want_big_ranked_df = want_big_num_df.rank(ascending=False).astype(int)
    want_small_ranked_df = want_small_num_df.rank(ascending=True).astype(int)
    ranked_df = pd.concat([want_big_ranked_df, want_small_ranked_df], axis=1)
    ranked_df["Avg. Cat. Rank"] = ranked_df.mean(axis=1)

    # Concatenate with non-numeric columns
    ranked_df = pd.concat([ranked_df, raw_stats_df.select_dtypes(exclude="number")], axis=1)

    return ranked_df[list(const.ALL_DATA_RANKED_TABLE_DEF.keys())].sort_values(by="Standing")


def get_league_cat_raw_stats_df(league: League) -> pd.DataFrame:
    """Get every team's stats for only roto categories."""
    league_stats = []
    for team in league.team_dict.values():
        temp_dict = deepcopy(team.stats)
        temp_dict["Team"] = team.team_name
        temp_dict["Standing"] = team.standing
        league_stats.append(temp_dict)

    df = pd.DataFrame(league_stats)

    df = df.astype(const.CAT_ONLY_RAW_DATA_TABLE_DEF)
    return df[list(const.CAT_ONLY_RAW_DATA_TABLE_DEF.keys())].sort_values(by="Standing")


def get_league_cat_data_rankings(league: League) -> pd.DataFrame:
    """Get every team's ranking for only roto categories."""
    raw_stats_df = get_league_all_raw_stats_df(league)
    # Rank only numeric columns
    want_big_num_df = raw_stats_df[const.WANT_BIG_NUM]
    want_small_num_df = raw_stats_df[const.WANT_SMALL_NUM]
    want_big_ranked_df = want_big_num_df.rank(ascending=False).astype(int)
    want_small_ranked_df = want_small_num_df.rank(ascending=True).astype(int)
    ranked_df = pd.concat([want_big_ranked_df, want_small_ranked_df], axis=1)
    ranked_df["Avg. Cat. Rank"] = ranked_df.mean(axis=1)

    # Concatenate with non-numeric columns
    ranked_df = pd.concat([ranked_df, raw_stats_df.select_dtypes(exclude="number")], axis=1)
    return ranked_df[list(const.CAT_ONLY_DATA_RANKED_TABLE_DEF.keys())].sort_values(by="Standing")


def get_average_team_stats(team: Team, num_days: int) -> pd.DataFrame:
    """Get Stats for team averaged over specified number of days From todays date."""
    SUPPORTED_TIMES = [30, 15, 7]

    if num_days not in SUPPORTED_TIMES:
        raise ValueError(f"num_days must be one of {SUPPORTED_TIMES}")

    stat_key = f"{const.YEAR}_last_{num_days}"
    player_avgs = {player.name: player.stats[stat_key].get("avg", {}) for player in team.roster}
    player_avgs = pd.DataFrame(player_avgs).T.fillna(0)
    pd.set_option("future.no_silent_downcasting", True)  # otherwise FutureWarning
    return player_avgs.replace("Infinity", 0).round(2)  # Replace Infinity with 0 kinda hacky but eh


def agg_player_avgs(
    seven_day_stats: pd.DataFrame, fifteen_day_stats: pd.DataFrame, thirty_day_stats: pd.DataFrame
) -> pd.DataFrame:
    """Aggregate player averages over different timeframes."""

    avg_seven_day_stats = seven_day_stats.aggregate("mean")
    avg_fifteen_day_stats = fifteen_day_stats.aggregate("mean")
    avg_thirty_day_stats = thirty_day_stats.aggregate("mean")
    agg_stats = pd.DataFrame(
        {
            "Past 7 Days": avg_seven_day_stats[const.NINE_CATS],
            "Past 15 Days": avg_fifteen_day_stats[const.NINE_CATS],
            "Past 30 Days": avg_thirty_day_stats[const.NINE_CATS],
        }
    )
    return agg_stats


def get_team_breakdown(team_cat_ranks: dict) -> tuple[dict, dict, dict]:
    """Given a row from the league rankings dataframe, parse the team's strengths, weaknesses, and punts.

    Args:
        team_cat_ranks (dict): A row from the league rankings dataframe.

        Returns:
        strengths (list): The categories in which the team excels.
        weaknesses (list): The categories in which the team is average.
        punts (list): The categories in which the team is weak."""
    strengths = []
    weaknesses = []
    punts = []

    for cat in const.NINE_CATS:
        if team_cat_ranks[cat] <= 4:
            strengths.append({"label": cat, "value": team_cat_ranks[cat]})
        elif team_cat_ranks[cat] >= 8:
            punts.append({"label": cat, "value": team_cat_ranks[cat]})
        else:
            weaknesses.append({"label": cat, "value": team_cat_ranks[cat]})
    return strengths, weaknesses, punts


def get_prompt(prompt_map: dict):
    """
    Returns a value from the dictionary based on the weighted probability.

    :param prompt_map: A dictionary where keys are percentages (adding up to 1.0) and values are strings.
    :return: A randomly selected value based on the key percentages.
    """
    rand_val = random.random()  # Random float between 0 and 1.
    cumulative = 0

    for percent, prompt in sorted(prompt_map.items()):
        cumulative += percent
        if rand_val < cumulative:
            return prompt


def get_mainpage_joke():
    client = Groq()
    prompt = get_prompt(prompts.mainpage_prompt_map)
    chat_completion = client.chat.completions.create(messages=prompt, model="llama3-8b-8192")
    return chat_completion.choices[0].message.content


def get_teamviewer_joke(team_name):
    client = Groq()
    prompt = [
        {
            "role": "system",
            "content": "Be a witty and kind of offensive when responding. Speak as an expert on fantasy basketball. Don't repeat yourself, and make sure to keep your sentences fresh.",
        },
        {
            "role": "user",
            "content": f"Roast the team name choice of: '{team_name}'. Limit response to 100 characters",
        },
    ]
    chat_completion = client.chat.completions.create(messages=prompt, model="llama3-8b-8192")
    return chat_completion.choices[0].message.content


def get_league_box_scores(league: League):
    """Get the matchups for the current week."""
    box_scores = league.box_scores(league.currentMatchupPeriod)
    return box_scores


def get_matchup_score_df(matchup: Matchup):
    """Get the score dataframe for a given matchup."""
    home_team_name = matchup.home_team.team_abbrev
    away_team_name = matchup.away_team.team_abbrev
    home_df = (
        pd.DataFrame(matchup.home_team_cats)
        .T.drop(columns=["result"])
        .rename(columns={"score": home_team_name})
    )
    away_df = (
        pd.DataFrame(matchup.away_team_cats)
        .T.drop(columns=["result"])
        .rename(columns={"score": away_team_name})
    )
    combined_df = pd.concat([home_df, away_df], axis=1)
    combined_df[f"{home_team_name}-{away_team_name}"] = (
        combined_df[home_team_name] - combined_df[away_team_name]
    )
    combined_df = combined_df.astype(float).round(2)
    return combined_df


if __name__ == "__main__":
    pass
