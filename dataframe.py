import datetime
import json
import logging
import pathlib
import re
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd

from logging_config import config_logger
from scrapper import CACHE, retrieve_games

GAMES_CSV = CACHE / "games_csv"
THINKING_TIME_CSV = CACHE / "thinking_time_csv"


def games_to_csv(player_id, use_cache=True, max_pages=100):
    games_csv = GAMES_CSV / f"{player_id}.csv"
    if games_csv.exists() and games_csv.is_file():
        logging.debug("Games csv is already cached")
        return

    games = retrieve_games(player_id, use_cache, max_pages)
    rows = [game.__dict__ for game in games]
    GAMES_CSV.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(games_csv)


def thinking_time_to_csv(table_id=123456789):
    # TODO: retrieve thinking time from id
    thinking_time_csv = THINKING_TIME_CSV / f"{table_id}.csv"
    if thinking_time_csv.exists() and thinking_time_csv.is_file():
        logging.debug("Thinking time csv is already cached")
        return

    path = pathlib.Path("data_files/parsed_data.json")
    with path.open() as file_handler:
        parsed_data = json.load(file_handler)
    parsed_df = pd.DataFrame(parsed_data)

    THINKING_TIME_CSV.mkdir(parents=True, exist_ok=True)
    parsed_df.to_csv(thinking_time_csv, index=False)


def duration_to_timedelta(duration):
    DURATION_RE = re.compile(r"(?P<days>\d+) days (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)")
    match = DURATION_RE.match(duration)
    if not match:
        return

    return datetime.timedelta(**{parameter: int(duration) for parameter, duration in match.groupdict().items()})


def get_time_by_player(games_df):
    time_by_player = dict()
    for _, row in games_df.iterrows():
        for player in row["player_names"].split(","):
            time_by_player[player] = time_by_player.get(player, 0) + int(
                duration_to_timedelta(row["duration"]).total_seconds()
            )
    return time_by_player


def group_smaller_values(value_by_label: Dict, max_values=10):
    if len(value_by_label) <= max_values:
        return value_by_label

    reduced_dict = dict(value_by_label)
    for key, value in sorted(reduced_dict.items(), key=lambda item: item[1])[:-max_values]:
        reduced_dict["others"] = reduced_dict.get("others", 0) + value
        del reduced_dict[key]
    return reduced_dict


def pie_chart(value_by_label: Dict):
    fig, ax = plt.subplots()
    size = 0.3
    _, texts = ax.pie(
        value_by_label.values(), labels=value_by_label.keys(), radius=1, wedgeprops=dict(width=size, edgecolor="w")
    )
    for text in texts:
        text.set_color("white")

    return fig


if __name__ == "__main__":
    config_logger()
    # games_to_csv(123456789)
    # thinking_time_to_csv()
    # print(duration_to_timedelta("0 days 00:16:43"))
