# Collect Info on Start.gg Tournaments for automatic Calendar Updates

Pulls info on select tournaments on start.gg and uses this information to create google calendar events or discord events.

## Example Usage of StartGG Module for Querying Tournaments

Let's walk through a quick example on how you might pull tournament info from the startgg api class `TournamentPuller`.

```python
from TournamentPuller import TournamentPuller
from constants import STARTGGAPIKEY

# initiate an object of class TournamentPuller to get tournament data
tp = TournamentPuller(apikey=STARTGGAPIKEY, state="NC")

# initiate results by state, we already provided state at the initition
# step so we dont need to pass that in agin here
# note that we also could have initiated by a list of owner ids
tp.initiate_by_state()

# afer we get state results lets only look at tournaments that run certain games
# there are also other filter options to choose from that can be used once a 
# list is initiated
tp.filter_by_game(game_list=['game/street-fighter-6', 'game/guilty-gear-strive'])

# check out the results
print(tp.tournament_list)
```