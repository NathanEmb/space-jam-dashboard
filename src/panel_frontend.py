import datetime as dt
import logging

import panel as pn

import backend as be

pn.extension("tabulator")

logger = logging.getLogger()


class LeagueData:
    def __init__(self):
        self.data = be.get_league()
        self.last_updated = dt.datetime.now()

    def update(self):
        self.data = be.get_league()
        self.last_updated = dt.datetime.now()


def get_dataframe(mode: str, league_data: LeagueData):
    logger.info(f"Returning League Wide stats Dataframe for {league_data.data.league_id}")
    if mode == "All Data - Raw Stats":
        df = be.get_league_all_raw_stats_df(league_data.data)
    elif mode == "All Data - Ranked":
        df = be.get_league_all_raw_data_rankings(league_data.data)
    elif mode == "Categories - Raw Stats":
        df = be.get_league_cat_raw_stats_df(league_data.data)
    elif mode == "Categories - Rankings":
        df = be.get_league_cat_data_rankings(league_data.data)
    return df


def app():
    league_data = LeagueData()

    mode = pn.widgets.Select(
        name="Mode",
        options=[
            "Categories - Rankings",
            "Categories - Raw Stats",
            "All Data - Ranked",
            "All Data - Raw Stats",
        ],
    )
    refresh_button = pn.widgets.Button(
        name="Refresh Stats"
    )  # doesn't work. my interactive table is f-d beyond comprehension

    interactive_df = pn.bind(get_dataframe, mode=mode, league_data=league_data)
    interactive_table = pn.widgets.Tabulator(interactive_df, theme="site", show_index=False)
    return pn.template.ReactTemplate(
        title="Space Jam Dashboard",
        sidebar=[refresh_button, mode],
        main=[interactive_table],
        sidebar_width=150,
    )


app().servable()
