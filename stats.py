from collections import defaultdict
import datetime

class Stats():
    def __init__(self, games) -> None:
        self.games = games

        self.number_of_games = len(games)
        self.different_games_count = 0
        self.different_games = set()
        self.total_time_played = datetime.timedelta(0)
        self.total_time_by_date = defaultdict(datetime.timedelta)

        for game in games:
            self.__update_stats(game)

    def __update_stats(self, game):
        self.different_games.add(game.game_name)
        self.different_games_count = len(self.different_games)
        self.total_time_played += game.duration
        self.total_time_by_date[game.start.date().strftime('%Y-%m-%d')] += game.duration
        # self.total_time_by_date[game.start.timestamp()] += game.duration

    def get_total_time_by_date_json(self):
        def get_epoch_time(date_str):
            return int(datetime.datetime.strptime(date_str, '%Y-%m-%d').timestamp())
        return {str(get_epoch_time(date)): self.total_time_by_date[date].total_seconds()/60 for date in self.total_time_by_date}

    def get_games_by_date(self):
        ret = {}
        for game in self.games:
            day_date_str = str(game.start.date().strftime('%Y-%m-%d'))
            day_date_str = f'{day_date_str}T03:00:00.000Z'
            if day_date_str not in ret:
                ret[day_date_str] = {}
            if 'details' not in ret[day_date_str]:
                 ret[day_date_str]['details'] = []
            if 'total' not in ret[day_date_str]:
                ret[day_date_str]['total'] = 0
            
            ret[day_date_str]['details'].append({"name": game.pretty_game_name, "date": str(game.start.isoformat()), "value": game.duration.total_seconds()})
            ret[day_date_str]['total'] += game.duration.total_seconds()

        correct_ret = []
        for item in ret.keys():
            correct_ret.append({'date': item, 'details': ret[item]['details'], 'total': ret[item]['total']})
        return correct_ret