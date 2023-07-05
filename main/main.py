# Ves
import discord
from discord import app_commands
from discord.ext import commands
import os
from twelvedata import TDClient
from typing import Optional

TOKEN = os.getenv("DISCORD_TOKEN_VES")
API_KEY = os.getenv("API_KEY_TD")

td = TDClient(apikey = API_KEY)

bot = commands.Bot(command_prefix = ".", intents = discord.Intents.default())

@bot.event
async def on_ready():

    try:
        
        synced = await bot.tree.sync()
        print(f"Succesfully synced {len(synced)} command(s)!")

    except Exception as e:

        print(e)

    print(f"{bot.user.name} is cooking!")

# Slash Command: /say [say_this]
@bot.tree.command(name = "say", description = "Tell Ves to say something.")
@app_commands.describe(say_this = "What do you want me to say?")
async def say(interaction: discord.Interaction, say_this: Optional[str] = None):

    await interaction.response.send_message(f"{interaction.user.mention} told me to say: '**{say_this}**'") # Add 'ephemeral = True' to make it visible only to the user

@bot.tree.command(name = "watchlist", description = "Interact with your stocks watchlist.")
@app_commands.describe(action = "Add | add a stock to your watchlist, Remove | remove a stock from your watchlist, Choose | get a specific stock from your watchlist")


bot.run(TOKEN)