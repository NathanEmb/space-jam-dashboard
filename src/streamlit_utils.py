import streamlit as st


def create_metric_grid(data: dict[str, float], num_cats_per_row: int = 2):
    
    while data:
        inner_cols = st.columns(num_cats_per_row)
        for i in range(num_cats_per_row):
            try:
                cat = list(data.keys())[0]
            except IndexError:
                break
            val = data.pop(cat)
            inner_cols[i].metric(cat, val)
