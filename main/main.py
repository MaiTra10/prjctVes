# Ves
import discord
from discord import app_commands
from discord.ext import commands
# OS import for loading environment variable
import os
# get token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN_VES')
# initialize bot with '.' prefix and feault intents
bot = commands.Bot(command_prefix = ".", intents = discord.Intents.default())
# Initial bot event
@bot.event
async def on_ready():
    # Try to sync slash commands, catch Exception and print it
    try:
        
        synced = await bot.tree.sync()
        print(f"Succesfully synced {len(synced)} command(s)!")

    except Exception as e:

        print(e)

    print(f"{bot.user.name} is cooking!")
# Slash Command: /say [say_this]
@bot.tree.command(name = "say", description = "Tell Ves to say something.")
@app_commands.describe(say_this = "What do you want me to say?")
async def say(interaction: discord.Interaction, say_this: str):
    await interaction.response.send_message(f"{interaction.user.mention} told me to say: '{say_this}'.") # Add 'ephemeral = True' to make it visible only to the user
# Run bot using unique token
bot.run(TOKEN)