import streamlit as st


def create_metric_grid(data: dict[str, float], num_cats_per_row: int = 3):
    j = 0
    rows_of_cols = []
    while data:
        rows_of_cols.append(st.columns(num_cats_per_row))
        for i in range(num_cats_per_row):
            try:
                cat = list(data.keys())[0]
            except IndexError:
                break
            val = data.pop(cat)
            rows_of_cols[j][i].metric(cat, val)
        j += 1
