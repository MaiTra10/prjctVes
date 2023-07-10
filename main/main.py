# Ves
import discord
import os
import requests
import json
from discord import app_commands
from discord.ext import commands
from typing import Optional

TOKEN = os.getenv("DISCORD_TOKEN_VES")
API_KEY = os.getenv("API_KEY_TD")

bot = commands.Bot(command_prefix = ".", intents = discord.Intents.default())

def api(http_method, method, params):

    url = "https://4qq4mnhpug.execute-api.us-west-2.amazonaws.com/prod/" + method

    if http_method == "POST":

        resp = requests.post(url, params = params)

    elif http_method == "GET":

        resp = requests.get(url, params = params)

    else:

        resp = requests.delete(url, params = params)

    return {

        "StatusCode": resp.status_code,
        "body": resp.text

    }

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

@bot.tree.command(name = "wl_add", description = "Add an entry to your watchlist")
@app_commands.describe(choice = "Choose either 'steam' or 'stock'", name = "Steam: Exact name of item and wear (if any) at end in brackets | Stock: '[ticker]:[exchange]'")
async def wl_add(interaction: discord.Interaction, choice: str, name:str):

    await interaction.response.send_message(f"User ID: {interaction.user.id}\nChoice: {choice}\nName: {name}")

bot.run(TOKEN)