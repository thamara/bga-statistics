from jinja2 import Environment, FileSystemLoader
from scrapper import retrieve_games
from stats import Stats
import os

from logging_config import config_logger, logging

player_id = 86798513


def main():
    config_logger()
    games = retrieve_games(player_id=player_id)
    stats = Stats(games)

    logging.info(f"Total time played: {stats.total_time_played}")
    logging.info(f"Number of games played: {stats.number_of_games}")

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    template = env.get_template("stats.html")
    output = template.render(
        stats=stats, heatmap_data=stats.get_games_by_date(), normalized_game_time=stats.get_normalized_time_by_game()
    )

    filename = "output/stats.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
