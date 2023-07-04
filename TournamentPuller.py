import json
from datetime import datetime, timedelta
from startgg_funcs import get_state_tournaments, get_owners_tournaments


class TournamentPuller:

    def __init__(
            self, apikey, game_list=None, owner_list=None, state=None,
            start_date=datetime.today(),
            end_date=datetime.today() + timedelta(days=30)):

        self.key = apikey
        self.tournament_list = None
        self.game_list = game_list
        self.owner_list = owner_list
        self.state = state
        self.end_date = end_date
        self.start_date = start_date

    def initiate_by_state(self, state=None):
        if state is None:
            state = self.state

        if not isinstance(state, str):
            raise TypeError("'state' must be of type string to run.")

        self.tournament_list = get_state_tournaments(
            state=self.state, start_date=self.start_date, end_date=self.end_date, key=self.key)

    def initiate_by_owner(self, owner_list=None):
        if owner_list is None:
            owner_list = self.owner_list

        if not isinstance(owner_list, list):
            raise TypeError("'owner_list' must be a list of length at least 1 with string types.")

        if len(owner_list) == 0:
            raise TypeError("'owner_list' must be a list of length at least 1 with string types.")

        if not owner_list[0]:
            raise TypeError("'owner_list' must be a list of length at least 1 with string types.")

        self.tournament_list = get_owners_tournaments(
            owner_list, key=self.key, start_date=self.start_date, end_date=self.end_date)

    def filter_by_game(self, game_list=None):
        if game_list is None:
            game_list = self.game_list

        if not isinstance(game_list, list):
            raise TypeError("'game_list' must be a list of length at least 1 with string types.")

        if len(game_list) == 0:
            raise TypeError("'game_list' must be a list of length at least 1 with string types.")

        if not game_list[0]:
            raise TypeError("'game_list' must be a list of length at least 1 with string types.")

        self.tournament_list = [
            i for i in self.tournament_list if any(
                [j in game_list for j in [k["videogame"]["slug"] for k in i["events"]]])]

    def filter_by_owner(self, owner_list=None):
        if owner_list is None:
            owner_list = self.owner_list

        if not isinstance(owner_list, list):
            raise TypeError("'owner_list' must be a list of length at least 1 with string types.")

        if len(owner_list) == 0:
            raise TypeError("'owner_list' must be a list of length at least 1 with string types.")

        if not owner_list[0]:
            raise TypeError("'owner_list' must be a list of length at least 1 with string types.")

        self.tournament_list = [
            i for i in self.tournament_list if i["owner"]["id"] in owner_list]

    def filter_by_state(self, state=None):
        if state is None:
            state = self.state

        if not isinstance(state, str):
            raise TypeError("'state' must be of type string to run.")

        self.tournament_list = [
            i for i in self.tournament_list if i["addrState"] == state]

    def write_tournament_details(self, file):
        json_object = json.dumps(self.tournament_list, indent=4)

        # Writing to sample.json
        with open(file, "w") as outfile:
            outfile.write(json_object)


if __name__ == '__main__':
    from constants import STARTGGAPIKEY
    from options import VALID_GAMES, OWNER_LIST

    tp = TournamentPuller(apikey=STARTGGAPIKEY, game_list=VALID_GAMES, owner_list=OWNER_LIST, state="NC")
    tp.initiate_by_state()
    tp.filter_by_game()
