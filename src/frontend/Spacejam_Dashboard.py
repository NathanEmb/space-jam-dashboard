import matplotlib.pyplot as plt
import streamlit as st

import src.backend as be
from src.frontend.streamlit_utils import page_setup

page_setup()

league_data = st.session_state.league_data
teams = st.session_state.teams
league_df = st.session_state.league_df

# Sidebar for page selection
st.sidebar.success("Welcome to the Space Jammers Lounge, written by the Tatums.")
st.sidebar.subheader("And now, a joke powered by AI 🤖")
try:
    st.sidebar.write(be.get_mainpage_joke())
except Exception:
    st.sidebar.write("The bots broke..")

# Main Page content
st.title("Space Jammers Lounge")
st.subheader("About")
st.markdown("A site to lookup fantasy basketball rankings for Space Jammers.")
st.header("Category Rankings")
st.subheader("Green is good", divider=True)
st.info("On mobile, landscape makes this more usable.\n", icon="ℹ️")
st.write("")
gyr = plt.colormaps["RdYlGn"].reversed()
league_df = league_df.set_index("Team")
league_df_styled = league_df.style.background_gradient(cmap=gyr)
st.dataframe(league_df_styled, width="stretch", height=460, on_select="ignore")
