SPACEJAM_LEAGUE_ID = 233677
YEAR = 2025

ALL_RAW_DATA_TABLE_DEF = {
    "Team": str,
    "Standing": int,
    "PTS": int,
    "BLK": int,
    "STL": int,
    "AST": int,
    "REB": int,
    "TO": int,
    "FGM": int,
    "FGA": int,
    "FTM": int,
    "FTA": int,
    "3PM": int,
    "FG%": float,
    "FT%": float,
}

ALL_DATA_RANKED_TABLE_DEF = {
    "Team": str,
    "Standing": int,
    "Avg. Cat. Rank": int,
    "PTS": int,
    "BLK": int,
    "STL": int,
    "AST": int,
    "REB": int,
    "TO": int,
    "FGM": int,
    "FGA": int,
    "FTM": int,
    "FTA": int,
    "3PM": int,
    "FG%": int,
    "FT%": int,
}

CAT_ONLY_RAW_DATA_TABLE_DEF = {
    "Team": str,
    "Standing": int,
    "PTS": int,
    "BLK": int,
    "STL": int,
    "AST": int,
    "REB": int,
    "TO": int,
    "3PM": int,
    "FG%": float,
    "FT%": float,
}

CAT_ONLY_DATA_RANKED_TABLE_DEF = {
    "Team": str,
    "Standing": int,
    "Avg. Cat. Rank": int,
    "PTS": int,
    "BLK": int,
    "STL": int,
    "AST": int,
    "REB": int,
    "TO": int,
    "3PM": int,
    "FG%": int,
    "FT%": int,
}

WANT_BIG_NUM = [
    "PTS",
    "BLK",
    "STL",
    "AST",
    "REB",
    "FGM",
    "FGA",
    "FTM",
    "FTA",
    "3PM",
    "FG%",
    "FT%",
]

WANT_SMALL_NUM = ["Standing", "TO"]
