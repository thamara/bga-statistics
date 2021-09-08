import datetime
from prettifier import get_pretty_name


class Game:
    """Represents a table (or game). Example of json:
    {
     'table_id': '197451485', 'game_name': 'dicehospital', 'game_id': '1321',
     'start': '1630119894', 'end': '1630123920', 'concede': '0', 'unranked': '0',
     'normalend': '1', 'players': '85808177,90120944,89818831,86798513',
     'player_names': 'araujoarthur0,barbara1508,dleite,tkcandrade', 'scores': '51,41,38,32',
     'ranks': '1,2,3,4', 'elo_win': '0', 'elo_penalty': '', 'elo_after': '1363',
     'arena_win': None, 'arena_after': '1.1500'
    }
    """

    def __init__(self, table_id, game_name, game_id, start, end, players, player_names, scores, ranks) -> None:
        self.table_id = table_id
        self.game_name = game_name
        self.pretty_game_name = get_pretty_name(self.game_name)
        self.game_id = game_id
        self.start = datetime.datetime.fromtimestamp(int(start))
        self.end = datetime.datetime.fromtimestamp(int(end))
        self.duration = self.end - self.start
        self.players = players
        self.player_names = player_names
        self.scores = scores
        self.ranks = ranks

    def __str__(self):
        return f"{self.game_name} ({self.game_id} - {self.duration})"
