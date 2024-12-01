import pandas as pd

from espn_api.basketball import League

import constants as const


def get_league(league_id: int = const.SPACEJAM_LEAGUE_ID, year: int = const.YEAR):
    return League(league_id, year)


def get_league_all_raw_stats_df(league: League):
    league_stats = []
    for team in league.teams:
        temp_dict = team.stats.copy()
        temp_dict["Team"] = team.team_name
        temp_dict["Standing"] = team.standing
        league_stats.append(temp_dict)

    df = pd.DataFrame(league_stats)

    df = df.astype(const.ALL_RAW_DATA_TABLE_DEF)
    return df[list(const.ALL_RAW_DATA_TABLE_DEF.keys())]


def get_league_all_raw_data_rankings(league: League):
    raw_stats_df = get_league_all_raw_stats_df(league)
    # Rank only numeric columns
    want_big_num_df = raw_stats_df[const.WANT_BIG_NUM]
    want_small_num_df = raw_stats_df[const.WANT_SMALL_NUM]
    want_big_ranked_df = want_big_num_df.rank(ascending=False).astype(int)
    want_small_ranked_df = want_small_num_df.rank(ascending=True).astype(int)
    ranked_df = pd.concat([want_big_ranked_df, want_small_ranked_df], axis=1)
    ranked_df["Avg. Cat. Rank"] = ranked_df.mean(axis=1)

    # Concatenate with non-numeric columns
    ranked_df = pd.concat(
        [
            ranked_df,
            raw_stats_df.select_dtypes(exclude="number"),
        ],
        axis=1,
    )

    return ranked_df[list(const.ALL_DATA_RANKED_TABLE_DEF.keys())]


def get_league_cat_raw_stats_df(league: League):
    league_stats = []
    for team in league.teams:
        temp_dict = team.stats.copy()
        temp_dict["Team"] = team.team_name
        temp_dict["Standing"] = team.standing
        league_stats.append(temp_dict)

    df = pd.DataFrame(league_stats)

    df = df.astype(const.CAT_ONLY_RAW_DATA_TABLE_DEF)
    return df[list(const.CAT_ONLY_RAW_DATA_TABLE_DEF.keys())]


def get_league_cat_data_rankings(league: League):
    raw_stats_df = get_league_all_raw_stats_df(league)
    # Rank only numeric columns
    want_big_num_df = raw_stats_df[const.WANT_BIG_NUM]
    want_small_num_df = raw_stats_df[const.WANT_SMALL_NUM]
    want_big_ranked_df = want_big_num_df.rank(ascending=False).astype(int)
    want_small_ranked_df = want_small_num_df.rank(ascending=True).astype(int)
    ranked_df = pd.concat([want_big_ranked_df, want_small_ranked_df], axis=1)
    ranked_df["Avg. Cat. Rank"] = ranked_df.mean(axis=1)

    # Concatenate with non-numeric columns
    ranked_df = pd.concat(
        [
            ranked_df,
            raw_stats_df.select_dtypes(exclude="number"),
        ],
        axis=1,
    )
    return ranked_df[list(const.CAT_ONLY_DATA_RANKED_TABLE_DEF.keys())]


if __name__ == "__main__":
    pass
