import json
from datetime import datetime, timedelta
from typing import Optional
from startgg_funcs import get_state_tournaments, get_owners_tournaments


class TournamentPuller:
    """Implementation of a class that pulls tournament information using
    start.gg's API. **NOTE:** This class is under development and does
    not provide backwards compatible guarantees.
    """
    def __init__(self,
                 api_key: str,
                 game_list: Optional[list[str]] = None,
                 owner_list: Optional[list[int]] = None,
                 state: str = '',
                 start_date: datetime = datetime.today(),
                 end_date: datetime = datetime.today() + timedelta(days=30)):
        """Creates a TournamentPuller object with defaults for queries and
        filters.

        Args:
            api_key: API key registered with start.gg. Instructions on getting
                an API key can be found at:
                https://developer.start.gg/docs/authentication
            game_list: a list of games to seek tournaments for
            owner_list: a list of start.gg owner ids (ints) to seek tournaments
                from
            state: the state in the US to limit events to
            start_date: a datetime object representing the lower bound of the
                window of time to search
            end_date: a datetime object representing the upper bound of the
                window of time to search
        """

        self.key = api_key
        self.tournament_list = None
        self.game_list = game_list
        self.owner_list = owner_list
        self.state = state
        self.end_date = end_date
        self.start_date = start_date

    def initiate_by_state(self, state: str = ''):
        """Pulls tournaments from a specific US state.
        Defaults to using the state in the TournamentPuller class if an empty
        string is provided.

        Args:
            state: two-character identifier for a US state, e.g. "NC"

        Raises:
            ValueError if an empty string is provided and present in the
                TournamentPuller class simultaneously.
        """
        if state == '' and self.state != '':
            state = self.state

        if state == '':
            raise ValueError("Must provide a valid state string.")

        self.tournament_list = get_state_tournaments(
            state=self.state,
            start_date=self.start_date,
            end_date=self.end_date,
            key=self.key)

    def initiate_by_owner(self, owner_list: Optional[list[int]] = None):
        """Pulls tournaments from a list of specific start.gg owner ids.
        Defaults to using the owner_list in the TournamentPuller class if no
        list is provided.

        Args:
            owner_list: a list of valid owner ids to include

        Raises:
            ValueError if no list is provided and one is not present in the
                TournamentPuller class simultaneously. Also raises on lists
                of length 0.
        """
        if owner_list is None and self.owner_list is not None:
            owner_list = self.owner_list

        if owner_list is None:
            raise ValueError(
                "'owner_list' or TournamentPuller.owner_list must not be None")

        if len(owner_list) == 0:
            raise ValueError(
                "'owner_list' must be a list of length at least 1 with int types."
            )

        self.tournament_list = get_owners_tournaments(
            owner_list,
            key=self.key,
            start_date=self.start_date,
            end_date=self.end_date)

    def filter_by_game(self, game_list: Optional[list[str]] = None):
        """Filters the results contained in the TournamentPuller by a list of
        games. Defaults to using the game list in the TournamentPuller class
        if one is not provided.

        Args:
            game_list: a list of valid games to include

        Raises:
            ValueError if no list is provided and one is not present in the
                TournamentPuller class simultaneously.
        """
        if game_list is None and self.game_list is not None:
            game_list = self.game_list

        if game_list is None:
            raise ValueError(
                "'game_list or TournamentPuller.game_list must not be None")

        if len(game_list) == 0:
            raise TypeError(
                "'game_list' must be a list of length at least 1 with string types."
            )

        self.tournament_list = [
            i for i in self.tournament_list if any([
                j in game_list
                for j in [k["videogame"]["slug"] for k in i["events"]]
            ])
        ]

    def filter_by_owner(self, owner_list: Optional[list[int]] = None):
        """Filters the results contained in the TournamentPuller by owner.
        Defaults to using the owner list in the TournamentPuller class if one
        is not provided.

        Args:
            owner_list: a list of valid owner ids to include

        Raises:
            ValueError if no list is provided and one is not present in the
                TournamentPuller class simultaneously.
        """
        if owner_list is None and self.owner_list is not None:
            owner_list = self.owner_list

        if owner_list is None:
            raise ValueError(
                "'owner_list' or TournamentPuller.owner_list must not be None")

        if len(owner_list) == 0:
            raise ValueError(
                "'owner_list' must be a list of length at least 1 with int types."
            )

        self.tournament_list = [
            i for i in self.tournament_list if i["owner"]["id"] in owner_list
        ]

    def filter_by_state(self, state: str = ''):
        """Filters the results contained in the TournamentPuller by state.
        Defaults to using the state in the TournamentPuller class if an empty
        string is provided.

        Args:
            state: two-character identifier for a US state, e.g. "NC"

        Raises:
            ValueError if an empty string is provided and present in the
                TournamentPuller class simultaneously.
        """
        if state == '' and self.state != '':
            state = self.state
        elif state == '':
            raise ValueError(
                "'state' or TournamentPuller.state cannot be an empty string")

        self.tournament_list = [
            i for i in self.tournament_list if i["addrState"] == state
        ]

    def write_tournament_details(self, file):
        """Writes the collected tournament details to a file in JSON format.
        
        Args:
            file: file to write to
        """
        json_object = json.dumps(self.tournament_list, indent=4)

        # Writing to sample.json
        with open(file, "w", encoding=str) as outfile:
            outfile.write(json_object)
            outfile.close()


if __name__ == '__main__':
    from constants import STARTGGAPIKEY
    from options import VALID_GAMES, OWNER_LIST

    tp = TournamentPuller(api_key=STARTGGAPIKEY,
                          game_list=VALID_GAMES,
                          owner_list=OWNER_LIST,
                          state="NC")
    tp.initiate_by_state()
    tp.filter_by_game()
