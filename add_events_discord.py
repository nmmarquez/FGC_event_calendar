
import discord
from datetime import datetime
from tournament_puller import TournamentPuller
import dotenv
import os
import time
from discord import app_commands
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


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    for e in await (await client.fetch_guild(os.environ['GUILD_ID'])).fetch_scheduled_events():
        print(await e.delete())
    print(f'We have logged in as {client.user}')

async def dump_events(guild,guild_events):
    for t in tp.tournament_list:
        if([event for event in guild_events if event.name == t['name']]):
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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

intents = discord.Intents.default()
@tree.command(name = "dumpevents", description = "Dumps NC Start.gg Events")
async def first_command(interaction):
    
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(content="Getting Events from Start.GG")
    tp.initiate_by_state("NC")
    tp.filter_by_game(game_list=['game/street-fighter-6', 'game/guilty-gear-strive'])
    guild = await client.fetch_guild(os.environ['GUILD_ID'])
    guild_events = await guild.fetch_scheduled_events()
    await interaction.followup.send(content="Loading Events")

    await dump_events(guild,guild_events)
    await interaction.followup.send(content="Done")
client.run(os.environ["BOT_TOKEN"])
