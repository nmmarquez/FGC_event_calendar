from pysmashgg.api import run_query
from datetime import datetime, timedelta


TOURNAMENTOWNERQUERY = '''
query TournamentsByOwner($page: Int!, $ownerId: ID!, $startTime: Timestamp!, $endTime: Timestamp!, $perPage: Int!) {
    tournaments(query: {
      perPage: $perPage
      page: $page
      sortBy: "startAt asc"
      filter: {
        ownerId: $ownerId
        afterDate: $startTime
        beforeDate: $endTime
      }
    }) {
    nodes {
      id
      name
      slug
      startAt
      endAt
      url
      venueAddress
      addrState
      timezone
      owner{
        name
        id
        player{
          id
          gamerTag
        }
      }
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
}
'''

TOURNAMENTSTATEQUERY = '''
query TournamentsByOwner($page: Int!, $state: String!, $startTime: Timestamp!, $endTime: Timestamp!, $perPage: Int!) {
    tournaments(query: {
      perPage: $perPage
      page: $page
      sortBy: "startAt asc"
      filter: {
        addrState : $state
        afterDate: $startTime
        beforeDate: $endTime
      }
    }) {
    nodes {
      id
      name
      slug
      startAt
      endAt
      url
      venueAddress
      addrState
      timezone
      owner{
        name
        id
        player{
          id
          gamerTag
        }
      }
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
}
'''


def get_owner_tournaments(
        owner, key, start_date=datetime.today(),
        end_date=datetime.today()+timedelta(days=30)):
    """
    Returns a list of slug names of tournaments occurring in a selected state
    within two given dates.

            Parameters:
                    owner (int): id string for owner
                    start_date (datetime): minimum date time to consider
                    end_date (datetime): maximum date time to consider
                    key (str): start.gg api key

            Returns:
                    tournament_list (list): list of tournament slugs
    """
    page_length = 200
    variables = {
        "ownerId": owner,
        "page": 1,
        "startTime": int(round(start_date.timestamp())),
        "endTime": int(round(end_date.timestamp())),
        "perPage": page_length
    }
    header = {"Authorization": "Bearer " + key}
    tournament_list = list()
    all_valid = True
    max_tries = 100
    while all_valid and variables["page"] < max_tries:
        owner_tournaments = run_query(TOURNAMENTOWNERQUERY, variables, header, True)["data"]["tournaments"]["nodes"]
        all_valid = len(owner_tournaments) == page_length
        tournament_list += owner_tournaments
        variables["page"] += 1

    return tournament_list


def get_state_tournaments(
        state, key, start_date=datetime.today(),
        end_date=datetime.today()+timedelta(days=30)):
    """
    Returns a list of slug names of tournaments occurring in a selected state
    within two given dates.

            Parameters:
                    state (str): id string for state
                    start_date (datetime): minimum date time to consider
                    end_date (datetime): maximum date time to consider
                    key (str): start.gg api key

            Returns:
                    tournament_list (list): list of tournament slugs
    """
    page_length = 200
    variables = {
        "state": state,
        "page": 1,
        "startTime": int(round(start_date.timestamp())),
        "endTime": int(round(end_date.timestamp())),
        "perPage": page_length
    }
    header = {"Authorization": "Bearer " + key}
    tournament_list = list()
    all_valid = True
    max_tries = 100
    while all_valid and variables["page"] < max_tries:
        state_tournaments = run_query(TOURNAMENTSTATEQUERY, variables, header, True)["data"]["tournaments"]["nodes"]
        all_valid = len(state_tournaments) == page_length
        tournament_list += state_tournaments
        variables["page"] += 1

    return tournament_list


def get_owners_tournaments(
        owner_list, key, start_date=datetime.today(),
        end_date=datetime.today()+timedelta(days=30)):
    """

    :param owner_list:
    :param key:
    :param start_date:
    :param end_date:
    :return:
    """

    tournament_list = list()

    for o in owner_list:
        tournament_list += get_owner_tournaments(o, key=key, start_date=start_date, end_date=end_date)

    return tournament_list


