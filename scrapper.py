import getpass
import json
import logging
import pathlib
import pickle
import requests

from models import Game


def get_user_info():
    password = ""
    email = ""
    try:
        with open(".security", "r") as security:
            security_json = json.load(security)
            password = security_json["password"]
            email = security_json["email"]
    except KeyError:
        if not email:
            email = input("BGA Email: ")
        if not password:
            password = getpass.getpass(prompt="Password: ")
    return email, password


CACHE = pathlib.Path(".cache")
GAMES_CACHE = CACHE / "games"


def get_cached_info(player_id):
    try:
        with (GAMES_CACHE / f"{player_id}").open("rb") as f:
            games = pickle.load(f)
        logging.info(f"Loaded cached games ({len(games)} in total)")
        return games
    except FileNotFoundError:
        pass


def retrieve_games(player_id, use_cache=True, max_pages=100):
    if use_cache:
        games = get_cached_info(player_id)
        if games:
            return games

    games = []
    with requests.session() as c:
        # Login to Board Game Arena
        email, password = get_user_info()

        url_login = "http://en.boardgamearena.com/account/account/login.html"
        prm_login = {
            "email": email,
            "password": password,
            "rememberme": "on",
            "redirect": "join",
            "form_id": "loginform",
        }
        r = c.post(url_login, params=prm_login)
        if r.status_code != 200:
            logging.error("Login failed")
            exit

        url = f"https://boardgamearena.com/gamestats/gamestats/getGames.html?player={player_id}"
        params = {"opponent_id": 0, "finished": 1, "updateStats": 0, "page": 1}

        for page in range(1, max_pages):
            logging.info(f"Retrieving page {page}")
            params["page"] = page
            r = c.get(url, params=params)
            if r.status_code != 200:
                break

            y = json.loads(r.text)
            if len(y["data"]["tables"]) == 0:
                break
            for i in y["data"]["tables"]:
                # print(i)
                games.append(
                    Game(
                        i["table_id"],
                        i["game_name"],
                        i["game_id"],
                        i["start"],
                        i["end"],
                        i["players"],
                        i["player_names"],
                        i["scores"],
                        i["ranks"],
                    )
                )

    GAMES_CACHE.mkdir(parents=True, exist_ok=True)
    with (GAMES_CACHE / f"{player_id}").open("wb") as f:
        pickle.dump(games, f)
    return games
