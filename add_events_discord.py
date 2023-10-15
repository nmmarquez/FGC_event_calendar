
import discord
from datetime import datetime
from TournamentPuller import TournamentPuller
import dotenv
import os
import time
import redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
dotenv.load_dotenv()

errors = []
if(not os.environ.get("STARTGGAPIKEY")):
    errors.append("STARTGGAPIKEY not found in environment variables")
if(not os.environ.get("GUILD_ID")):
    errors.append("GUILD_ID not found in environment variables")
if(not os.environ.get("BOT_TOKEN")):
    errors.append("BOT_TOKEN not found in environment variables")
if(len(errors) > 0):
    print("\n".join(errors))
    exit(1)
# initiate an object of class TournamentPuller to get tournament data
tp = TournamentPuller(apikey=os.environ["STARTGGAPIKEY"], state="NC")

# initiate results by state, we already provided state at the initiation
# step so we dont need to pass that in again here
# note that we also could have initiated by a list of owner ids
tp.initiate_by_state()

# after we get state results lets only look at tournaments that run certain games
# there are also other filter options to choose from that can be used once a
# list is initiated
tp.filter_by_game(
    game_list=['game/street-fighter-6', 'game/guilty-gear-strive'])
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for e in await (await client.fetch_guild(os.environ['GUILD_ID'])).fetch_scheduled_events():
        print(await e.delete())
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$dumpevents'):
        guild = await client.fetch_guild(os.environ['GUILD_ID'])

        for t in tp.tournament_list:
            if(redis_client.get(t['id'])):
                continue
            time.sleep(1)
            await guild.create_scheduled_event(privacy_level=discord.PrivacyLevel.guild_only,
                                               entity_type=discord.EntityType.external,
                                               name=t['name'],
                                               description=f"https://www.start.gg{t['url']}",
                                               location=f"{t.get('venueAddress','')}",
                                               start_time=datetime.fromtimestamp(
                                                   t["startAt"]).astimezone(),
                                               end_time=datetime.fromtimestamp(t["endAt"]).astimezone())
            redis_client.set(t['id'],1)

client.run(os.environ["BOT_TOKEN"])
