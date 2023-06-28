from pysmashgg import SmashGG
from pysmashgg.api import run_query
from constants import STARTGGAPIKEY
from datetime import datetime, timedelta

TOURNAMENTGAMESQUERY = '''query TournamentGames($tournamentId: ID!) {
  tournament(id: $tournamentId) {
    id
    name
    events{
      id
      videogame{
        slug
      }
    }
  }
}
'''

TOURNAMENTDETAILSQUERY = '''query TournamentGames($tournamentId: ID!) {
  tournament(id: $tournamentId) {
    id
    name
    slug
    startAt
    endAt
    url
    venueAddress
    timezone
    images{
      url
      type
    }
    events{
      id
      videogame{
        slug
      }
    }
  }
}
'''

VALID_GAMES = (
    'game/dragon-ball-fighterz', 'game/street-fighter-iii-3rd-strike', 'game/street-fighter-6',
    'game/guilty-gear-strive', 'game/tekken-7')


def get_tournament_games(tournament_id, key=STARTGGAPIKEY, auto_retry=True):
    """
    Get all games that are being run at a tournament.

    :param tournament_id: integer of tournament id
    :param key: startgg api key
    :param auto_retry: whether to retry api call if it fails
    :return: list of games being run at a tournament
    """
    variables = {"tournamentId": tournament_id}
    header = {"Authorization": "Bearer " + key}
    response = run_query(TOURNAMENTGAMESQUERY, variables, header, auto_retry)
    data = response["data"]["tournament"]["events"]
    games = [x["videogame"]["slug"] for x in data]
    return games


def get_tournament_details(tournament_id, key=STARTGGAPIKEY, auto_retry=True):
    """
    Get details of tournament

    :param tournament_id: integer of tournament id
    :param key: startgg api key
    :param auto_retry: whether to retry api call if it fails
    :return: list of dictionaries including tournament details
    """
    variables = {"tournamentId": tournament_id}
    header = {"Authorization": "Bearer " + key}
    response = run_query(TOURNAMENTDETAILSQUERY, variables, header, auto_retry)
    data = response["data"]["tournament"]
    return data


def get_state_tournaments(
        state, start_date=datetime.today(),
        end_date=datetime.today()+timedelta(days=30), key=STARTGGAPIKEY):
    """
    Returns a list of slug names of tournaments occurring in a selected state
    within two given dates.

            Parameters:
                    state (str): A two letter state indicator
                    start_date (datetime): minimum date time to consider
                    end_date (datetime): maximum date time to consider
                    key (str): start.gg api key

            Returns:
                    tournament_list (list): list of tournament slugs
    """
    smash = SmashGG(key, True)
    all_valid = True
    max_tries = 10
    attempt = 0
    tournament_list = list()
    fts = datetime.fromtimestamp
    while all_valid and attempt < max_tries:
        state_tournaments = smash.tournament_show_by_state(state, 1)
        start_times = [fts(x["startTimestamp"]) for x in state_tournaments]
        valid_times = [start_date < x < end_date for x in start_times]
        valid_indices = [i for i, x in enumerate(valid_times) if x]
        tournament_list += [state_tournaments[i]["id"] for i in valid_indices]
        all_valid = all(valid_times)
        attempt += 1

    return tournament_list


def filter_by_games(
        tournament_list,
        game_list=VALID_GAMES,
        key=STARTGGAPIKEY):
    """
    Given a tournament list, returns tournament details only for those
    tournaments hosting events with certain games.

    :param tournament_list: list of tournament ids
    :param game_list: list of valid game slugs to filter to
    :param key: startgg api key
    :return: list of tournament dictionary details
    """
    valid_tournaments = list()
    for t in tournament_list:
        t_game_list = get_tournament_games(t, key=key)
        if any(x in game_list for x in t_game_list):
            valid_tournaments.append(get_tournament_details(t, key=key))

    return valid_tournaments


if __name__ == '__main__':
    # this takes a couple of minutes to run
    # get all events which are happening in NC in the next month
    nc_events = get_state_tournaments("NC")
    # filter down to just fgc games
    nc_fgc_events = filter_by_games(nc_events)
    print(nc_fgc_events)
