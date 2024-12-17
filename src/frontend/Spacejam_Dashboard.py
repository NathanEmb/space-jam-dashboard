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
st.sidebar.write(be.get_mainpage_joke())

# Main Page content
st.title("Space Jammers Lounge")
st.subheader("About")
st.markdown(
    "This site serves two purposes: \n 1. Be a fun project for me to work on. \n 2. Provide some more data to everyone who isn't already paying for a fancy schmancy site already."
)
st.markdown(
    "I hope you find this at minimum, mildly interesting, and at best, useful! Scroll down to see the first bit of data I worked out, and visit the sidebar to see a couple other pages."
)
st.header("Category Rankings")
st.subheader("Green is good", divider=True)
st.markdown(
    "This was the first bit of data that I wanted to understand when I was left with my head in my hands after a loss to Will saying 'What are the Tatum's good for?'. It shows each team's ranking per category, hopefully providing insight into punt strategies (or just seeing that your team sucks)."
)
st.info("On mobile, landscape makes this more usable.\n", icon="ℹ️")
st.write("")
gyr = plt.colormaps["RdYlGn"].reversed()
league_df = league_df.set_index("Team")
league_df_styled = league_df.style.background_gradient(cmap=gyr)
st.dataframe(league_df_styled, use_container_width=True, height=460, on_select="ignore")
