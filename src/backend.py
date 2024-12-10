from copy import deepcopy

import pandas as pd
from espn_api.basketball import League, Team

import src.constants as const


def get_league(league_id: int = const.SPACEJAM_LEAGUE_ID, year: int = const.YEAR) -> League:
    """Get the league object for the specified league_id and year."""
    league = League(league_id, year)
    league.teams = {team.team_name: team for team in league.teams}
    return league


def get_league_all_raw_stats_df(league: League) -> pd.DataFrame:
    """Get every team's stats for all categories."""
    league_stats = []
    for team in league.teams.values():
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
    for team in league.teams.values():
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
    return player_avgs.replace("Infinity", 0)  # Replace Infinity with 0 kinda hacky but eh


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
    strengths = {}
    weaknesses = {}
    punts = {}

    for cat in const.NINE_CATS:
        if team_cat_ranks[cat] <= 4:
            strengths[cat] = team_cat_ranks[cat]
        elif team_cat_ranks[cat] >= 8:
            punts[cat] = team_cat_ranks[cat]
        else:
            weaknesses[cat] = team_cat_ranks[cat]
    return strengths, weaknesses, punts


if __name__ == "__main__":
    pass
