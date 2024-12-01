import panel as pn
import backend as be

pn.extension("tabulator")

all_stats = be.get_league_all_raw_stats_df(be.get_league())
all_rankings = be.get_league_all_raw_data_rankings(be.get_league())
cat_stats = be.get_league_cat_raw_stats_df(be.get_league())
cat_rankings = be.get_league_cat_data_rankings(be.get_league())


def get_dataframe(mode: pn.widgets.Select):
    if mode == "All Data - Raw Stats":
        df = all_stats
    elif mode == "All Data - Ranked":
        df = all_rankings
    elif mode == "Categories - Raw Stats":
        df = cat_stats
    elif mode == "Categories - Rankings":
        df = cat_rankings
    return df


mode = pn.widgets.Select(
    name="Mode",
    options=[
        "Categories - Rankings",
        "Categories - Raw Stats",
        "All Data - Ranked",
        "All Data - Raw Stats",
    ],
)

interactive_df = pn.bind(get_dataframe, mode)

interactive_table = pn.widgets.Tabulator(interactive_df, theme="site", show_index=False)

pn.template.ReactTemplate(
    title="Space Jam Dashboard",
    sidebar=[mode],
    main=[interactive_table],
    sidebar_width=150,
).servable()
