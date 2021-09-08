from io import BytesIO
import logging
import datetime
import pandas as pd
import streamlit as st
from collections import OrderedDict

from dataframe import (
    duration_to_timedelta,
    pie_chart,
    GAMES_CSV,
    games_to_csv,
    get_time_by_player,
    group_smaller_values,
    THINKING_TIME_CSV,
    thinking_time_to_csv,
)
from logging_config import config_logger
from main import player_id

TABLE_ID = 123456789


def main():
    config_logger()

    logging.debug("Loading data")
    games_table, thinking_time_table = load_data()

    logging.debug("Rendering dashboard")
    st.set_page_config(
        page_title="BGA Analysis",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.title("Board Game Arena Analysis")
    dash_sidebar(games_table)
    dash_body(games_table, thinking_time_table)


def load_data():
    games_to_csv(player_id)
    thinking_time_to_csv()
    games_table = pd.read_csv(GAMES_CSV / f"{player_id}.csv")
    thinking_time_table = pd.read_csv(THINKING_TIME_CSV / f"{TABLE_ID}.csv")
    thinking_time_table["time"] = thinking_time_table["time"].apply(datetime.datetime.fromtimestamp)
    thinking_time_table = thinking_time_table.set_index(keys="time")
    return games_table, thinking_time_table


def dash_sidebar(games_table):
    st.sidebar.info(f"Total number of lines: {games_table.shape[0]}")
    if st.sidebar.checkbox("See results table"):
        st.header("Raw data")
        st.write(games_table)


def dash_body(games_table, thinking_time_table):
    columns = st.columns(2)

    with columns[0]:
        st.header("Games statistics")

        timedelta_duration = games_table["duration"].apply(duration_to_timedelta)
        total_time_played = sum(timedelta_duration, datetime.timedelta())
        st.subheader("Number of games played")
        st.code(f"{games_table.shape[0]}", language=None)
        st.markdown(f"`Play time: {total_time_played}`" "")

        st.subheader("Different games played")
        st.code(f"{games_table.game_id.unique().shape[0]}", language=None)

        games_frequency = games_table.pretty_game_name.value_counts()
        st.subheader("Top game")
        st.code(f"{games_frequency.index[0]}", language=None)
        st.markdown(f"`Played: {games_frequency[0]} times`" "")

    with columns[1]:
        st.header("Frenemies")
        st.subheader("The people you most played with (or against?)")

        time_by_player = get_time_by_player(games_table)
        time_by_player = OrderedDict(sorted(time_by_player.items(), key=lambda item: item[1])[:-1])
        top_friends = list(time_by_player.items())[:-3:-1]
        top_friends = [(key, datetime.timedelta(seconds=value)) for key, value in top_friends]
        st.markdown(f"`Top friends/rivals: {', '.join(f'{key}: {str(value)}' for key, value in top_friends)}`" "")

        # TODO: interactive chart instead of static image
        buffer = BytesIO()
        pie_chart(group_smaller_values(time_by_player)).savefig(buffer, format="png", transparent=True)
        st.image(buffer)

    st.header("Games distribution")
    st.bar_chart(games_table.pretty_game_name.value_counts())

    st.header(f"Game {TABLE_ID} thinking time")
    st.line_chart(thinking_time_table)


if __name__ == "__main__":
    main()
