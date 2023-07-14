# Ves
import discord
import os
import requests
import json
import simplejson as json
from discord import app_commands
from discord.ext import commands
from typing import Optional

TOKEN = os.getenv("DISCORD_TOKEN_VES")

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

        "statusCode": resp.status_code,
        "body": resp.text

    }

def validate_name(chosen, name):

    if chosen == "steam":

        params = {"requestType": "validate", "itemName": name}

    else:

        try:

            params = {"requestType": "validate", "ticker": name.split(":")[0], "exchange": name.split(":")[1]}

        except:

            return 400

    validate_resp  = api("GET", chosen, params)

    return validate_resp["statusCode"]

def get_both_item_list(items):
    
    steam_items = []
    stock_items = []

    steam_index = 0
    stock_index = 0

    for item in items:

        item_name = item["item"]

        if str(item["ctx"]).startswith(".v-"):
            
            steam_index += 1
            steam_items.append(f"{steam_index}. {item_name}")

        elif str(item["ctx"]).startswith(".s-"): 

            stock_index += 1
            stock_items.append(f"{stock_index}. {item_name}")

    steam_list_string = "\n> ".join(steam_items)
    stock_list_string = "\n> ".join(stock_items)

    return steam_list_string, stock_list_string

def get_steam_embed(items):

    embed = discord.Embed(title = "Steam Watchlist", color = 0x0175A7)

    for count, item in enumerate(items):
        
        count += 1

        item_name = item['item']

        steam_resp = api("GET", "steam", {"requestType": "basic", "itemName": item_name})

        steam_body = json.loads(steam_resp["body"])

        embed.add_field(name = f"{count}. {item_name}", value = f"{steam_body['lowest_price']}", inline = False)

    return embed

def get_stock_embed(items):

    embed = discord.Embed(title = "Stock Watchlist", color = 0x50C374)

    for count, item in enumerate(items):
        
        count += 1

        item_name = item['item']

        stock_resp = api("GET", "stock", {"requestType": "basic", "ticker": item_name.split(":")[0], "exchange": item_name.split(":")[1]})

        stock_body = json.loads(stock_resp["body"])

        if stock_body["% Change"] < 0.00:

            emoji = ":small_red_triangle_down:"

        elif stock_body["% Change"] > 0.00:

            emoji = "<:green_triangle_up:1129481299183284405>"

        else:

            emoji = ":white_small_square:"

        embed.add_field(name = f"{count}. {item_name} {emoji} {abs(stock_body['% Change'])}%", value = f"{stock_body['Current Price']}", inline = False)

    return embed

def get_specific_item_embed(chosen, item_name):
    
    if chosen == "steam":

        steam_resp = api("GET", "steam", {"requestType": "advanced", "itemName": item_name})

        steam_body = json.loads(steam_resp["body"])

        embed = discord.Embed(title = f"{item_name}", color = 0x0175A7)
        embed.set_thumbnail(url = f"{steam_body['imgURL']}")
        embed.add_field(name = "Lowest Price", value = f"{steam_body['lowest_price']}", inline = False)
        embed.add_field(name = "Volume", value = f"**{steam_body['volume']}** sold in the last 24 hours", inline = True)
        embed.add_field(name = "Median Sale Price", value = f"{steam_body['median_price']}", inline = True)

        return embed
    
    else:

        stock_resp = api("GET", "stock", {"requestType": "advanced", "ticker": item_name.split(":")[0], "exchange": item_name.split(":")[1]})

        stock_body = json.loads(stock_resp["body"])

        stock_parameters = list(stock_body.keys())[:-1]

        if stock_body["% Change"] < 0.00:

            emoji = ":small_red_triangle_down:"

        elif stock_body["% Change"] > 0.00:

            emoji = "<:green_triangle_up:1129481299183284405>"

        else:

            emoji = ":white_small_square:"

        embed = discord.Embed(title = f"{item_name} {emoji} {abs(stock_body['% Change'])}%", color = 0x50C374)

        for parameter in stock_parameters:

            embed.add_field(name = parameter, value = stock_body[parameter])

        if len(stock_parameters) == 8:

            embed.add_field(name = "", value = "")

        return embed

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
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def wl_add(interaction: discord.Interaction, choice: app_commands.Choice[str], name: str):

    await interaction.response.defer(ephemeral = True)

    chosen = choice.value

    valid = validate_name(chosen, name)

    if valid != 200:

        await interaction.followup.send(f"'{name}' is not a valid entry for a {chosen} watchlist!", ephemeral = True)
        return

    # 'name' is validated

    add_resp = api("POST", "add", {"for": chosen, "user": interaction.user.id, "itemToAdd": name})

    add_status = add_resp["statusCode"]

    if add_status == 409:

        await interaction.followup.send(f"'{name}' is already in your {chosen} watchlist!", ephemeral = True)
        return
    
    elif add_status == 403:

        await interaction.followup.send(f"You have reached the maximum number of entries for your {chosen} watchlist!", ephemeral = True)
        return
    
    else:

        await interaction.followup.send(f"'{name}' was successfully added to your {chosen} watchlist!", ephemeral = True)
        return

@bot.tree.command(name = "wl_remove", description = "Remove an entry from your watchlist")
@app_commands.describe(choice = "Choose either 'steam' or 'stock'", index = "Where in the list is the item you want to remove located? (1-10)")
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def wl_remove(interaction: discord.Interaction, choice: app_commands.Choice[str], index: app_commands.Range[int, 1, 10]):

    await interaction.response.defer(ephemeral = True)

    chosen = choice.value

    remove_resp = api("DELETE", "remove", {"for": chosen, "user": interaction.user.id, "index": index})

    remove_status = remove_resp["statusCode"]

    if remove_status == 403:

        await interaction.followup.send(f"Your {chosen} watchlist is empty!", ephemeral = True)
        return

    elif remove_status == 400:

        await interaction.followup.send(f"{remove_resp['body'].split(': ')[1]}", ephemeral = True)
        return
    
    else:

        await interaction.followup.send(f"'{json.loads(remove_resp['body'])['item']}' was successfully removed from your {chosen} watchlist!", ephemeral = True)
        return

@bot.tree.command(name = "wl", description = "Display your watchlist")
@app_commands.describe(choice = "Choose either 'steam', 'stock' or 'both'", index = "Which watchlist entry do you want to take a closer look at? (1-10)")
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def wl(interaction: discord.Interaction, choice: Optional[app_commands.Choice[str]] = "both", index: Optional[app_commands.Range[int, 1, 10]] = None):

    await interaction.response.defer(ephemeral = True)

    if choice != "both":

        chosen = choice.value

    else:

        chosen = choice

    if choice == "both" and index != None:

        embed = discord.Embed(title = "Error", description = f"You cannot specify an index without specifying a watchlist type (steam/stock).", color = 0xff0000)

        await interaction.followup.send(embed = embed, ephemeral = True)

        return

    if index == None:

        retrieve = "all"

    else:

        retrieve = "specific"

    get_resp = api("GET", "get", {"for": chosen, "user": interaction.user.id, "retrieve": retrieve, "index": index})

    get_status = get_resp["statusCode"]

    # Error check

    if get_status == 403:

        if chosen == "both":

            message = "Both of your watchlists are empty!"

        else:

            message = f"Your {chosen} watchlist is empty!"

        embed = discord.Embed(title = "Error", description = message, color = 0xff0000)

        await interaction.followup.send(embed = embed, ephemeral = True)

        return

    elif get_status == 400:

        embed = discord.Embed(title = "Error", description = f"{get_resp['body'].split(': ')[1]}", color = 0xff0000)

        await interaction.followup.send(embed = embed, ephemeral = True)

        return

    # No error in request

    if retrieve == "specific":

        item = json.loads(get_resp["body"])
        item_name = item['item']

        embed = get_specific_item_embed(chosen, item_name)

        await interaction.followup.send(embed = embed, ephemeral = True)
        return

    if chosen == "both":

        items = json.loads(get_resp["body"])

        steam_list_string, stock_list_string = get_both_item_list(items)

        embed = discord.Embed(title = "Watchlists", color = 0x7C437C)

        if steam_list_string != "":

            steam_prefix = "> "

        else:

            steam_prefix = ""

        if stock_list_string != "":

            stock_prefix = "> "

        else:

            stock_prefix = ""

        embed.add_field(name = "Steam", value = f"{steam_prefix}{steam_list_string}", inline = True)
        embed.add_field(name = "Stock", value = f"{stock_prefix}{stock_list_string}", inline = True)

        await interaction.followup.send(embed = embed, ephemeral = True)
        return
    
    elif chosen == "steam":

        items = json.loads(get_resp["body"])

        embed = get_steam_embed(items)

        await interaction.followup.send(embed = embed, ephemeral = True)
        return

    else:

        items = json.loads(get_resp["body"])

        embed = get_stock_embed(items)

        await interaction.followup.send(embed = embed, ephemeral = True)
        return
    
@bot.tree.command(name = "search", description = "Search for a specific CS:GO item or stock.")
@app_commands.describe(choice = "Choose either 'steam' or 'stock'", name = "Steam: Exact name of item and wear (if any) at end in brackets | Stock: '[ticker]:[exchange]'")
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def search(interaction: discord.Interaction, choice: app_commands.Choice[str], name: str):

    await interaction.response.defer(ephemeral = True)

    chosen = choice.value

    valid = validate_name(chosen, name)

    if valid != 200:

        await interaction.followup.send(f"'{name}' is not a valid stock/CS:GO item.", ephemeral = True)
        return

    # 'name' is validated

    embed = get_specific_item_embed(chosen, name)

    await interaction.followup.send(embed = embed, ephemeral = True)
    return

bot.run(TOKEN)