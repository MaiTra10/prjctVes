# Ves
import discord
import os
import requests
import simplejson as json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

def plot_tick_formatter(x, pos):
    
    return f"${x:.2f}"

def create_steam_plot(prices):

    price_list = []

    start_and_end_date = []

    for data in prices[::len(prices)-1]:

        start_and_end_date.append(data[0][:-7])

    for price in prices:

        price_list.append(price[1])

    graph, ax = plt.subplots()

    plt.plot(price_list, color = "#688F3E")
    plt.xticks([])
    plt.grid(color = "#4b4f52")
    plt.ylabel("(CAD)")
    plt.text(0, 0, start_and_end_date[0], ha='left', va='top', transform=ax.transAxes, color = "white")
    plt.text(0.8475, 0, start_and_end_date[1], ha='left', va='top', transform=ax.transAxes, color = "white")
    plt.rcParams["text.color"] = "white"

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(plot_tick_formatter))
    ax.yaxis.label.set_color("white")
    ax.set_facecolor("#2B2D31")
    ax.tick_params(colors = "#2B2D31")
    ax.spines['left'].set_color("#2B2D31")
    ax.spines['bottom'].set_color("#2B2D31")
    ax.spines['right'].set_color("#2B2D31")
    ax.spines['top'].set_color("#2B2D31")

    graph.set_facecolor("#2B2D31")

    ytick_labels = ax.get_yticklabels()

    for label in ytick_labels:

        label.set_color("white")


    file_name = "steam_graph.png"

    plt.savefig(file_name)

    return

def get_specific_item_embed(chosen, item_name):
    
    if chosen == "steam":

        steam_resp = api("GET", "steam", {"requestType": "advanced", "itemName": item_name})

        steam_body = json.loads(steam_resp["body"])

        embed = discord.Embed(title = f"{item_name}", color = 0x0175A7)
        try:
            embed.set_thumbnail(url = f"{steam_body['imgURL']}")
        except KeyError:
            print("Could not get Steam item image")
        embed.add_field(name = "Lowest Price", value = f"{steam_body['lowest_price']}", inline = False)
        embed.add_field(name = "Volume", value = f"**{steam_body['volume']}** sold in the last 24 hours", inline = True)
        embed.add_field(name = "Median Sale Price", value = f"{steam_body['median_price']}", inline = True)

        if steam_body["historyAvailable"] == True:

            create_steam_plot(steam_body["prices"])
            file = discord.File("steam_graph.png", "steam_graph.png")
            embed.set_image(url = "attachment://steam_graph.png")

        else:

            file = "empty"
            embed.set_footer(text = "*Graph is temporarily not available.*")

        return embed, file
    
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

        file = "empty"

        return embed, file

# Bot

@bot.event
async def on_ready():

    try:
        
        synced = await bot.tree.sync()
        print(f"Succesfully synced {len(synced)} command(s)!")

    except Exception as e:

        print(e)

    print(f"{bot.user.name} is cooking!")

    await bot.change_presence(status = discord.Status.online, activity= discord.Game("/help"))

@bot.tree.command(name = "help", description = "Get an overview of all the commands and how to use them.")
async def help(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral = False)

    embed = discord.Embed(title = "Ves' List of Commands", color = 0xE8E1E1)

    embed.add_field(name = "", value = f"*~ indicates an optional field*", inline = False)
    embed.add_field(name = f"<:green_plus:1129556140687097907> `/wl_add    <choice: [steam/stock]>  <name>`", value = "Add an entry to your watchlist (you are allowed a maximum of 10 entries per watchlist)\n", inline = False)
    embed.add_field(name = f"<:red_dash:1129556722248327208> `/wl_remove <choice: [steam/stock]>  <index: [1-10]>`", value = "Remove an entry from one of your watchlists\n", inline = False)
    embed.add_field(name = f":notepad_spiral: `/wl       ~<choice: [steam/stock]> ~<index: [1-10]>`", value = "Show your watchlist(s) or a watchlist entry\n> If you want to see an overview of both watchlists, provide no arguments\n> If you want to see a specific watchlist with prices, specify `choice`\n> If you want to see a detailed look at an entry in your watchlist, provide `choice` and `index`\n*Specific item queries can take up to 5 seconds*\n*Specific watchlist queries can take anywhere from 3 to 30 seconds (more time the more items there are in the list) so be patient*", inline = False)
    embed.add_field(name = f":mag_right: `/search    <choice: [steam/stock]>  <name>`", value = "Search for a specific Steam item or stock and get a detailed look", inline = False)
    embed.add_field(name = f"Formatting", value = "__Steam__\nCurrently only supports CS:GO items.\nTo ensure the item name is validated correctly, the name must be entered exactly as shown on the Steam market page (case-sensitive), and if it is an item with wear it must include the wear in brackets at the end of the item's name `ex. AK-47 | Slate (Field-Tested)'`.", inline = False)
    embed.add_field(name = "", value = "__Stock__\nThe retrieval of stock prices and data utilizes Google Finance so to ensure validation, use the format `[ticker]:[exchange]`. The current API supports all exchanges and futures currently available on Google Finance, discluding currencies and cryptocurrency.", inline = False)
    embed.add_field(name = "Links", value = "[My Github](https://github.com/MaiTra10) | [prjctVes Github Repo](https://github.com/MaiTra10/prjctVes)", inline = False)

    await interaction.followup.send(embed = embed, ephemeral = False)
    return

# Slash Command: /say [say_this]
@bot.tree.command(name = "say", description = "Tell Ves to say something.")
@app_commands.describe(say_this = "What do you want me to say?")
async def say(interaction: discord.Interaction, say_this: Optional[str] = None):

    await interaction.response.send_message(f"{interaction.user.mention} told me to say: '**{say_this}**'") # Add 'ephemeral = False' to make it visible only to the user

@bot.tree.command(name = "wl_add", description = "Add an entry to your watchlist")
@app_commands.describe(choice = "Choose either 'steam' or 'stock'", name = "Steam: Exact name of item and wear (if any) at end in brackets | Stock: '[ticker]:[exchange]'")
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def wl_add(interaction: discord.Interaction, choice: app_commands.Choice[str], name: str):

    await interaction.response.defer(ephemeral = False)

    chosen = choice.value

    if chosen == "steam":

        chosen_text = "Steam"

    else:

        chosen_text = "stocks"
        name = name.upper()

    valid = validate_name(chosen, name)

    if valid != 200:

        embed = discord.Embed(title = "Error", description = f"'{name}' is not a valid entry for a {chosen_text} watchlist!", color = 0xff0000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return

    # 'name' is validated

    add_resp = api("POST", "add", {"for": chosen, "user": interaction.user.id, "itemToAdd": name})

    add_status = add_resp["statusCode"]

    if add_status == 409:

        embed = discord.Embed(title = "Error", description = f"'{name}' is already in your {chosen_text} watchlist!", color = 0xff0000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return
    
    elif add_status == 403:

        embed = discord.Embed(title = "Error", description = f"You have reached the maximum number of entries for your {chosen_text} watchlist!", color = 0xff0000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return
    
    else:

        embed = discord.Embed(title = "", description = f"'{name}' was successfully added to your {chosen_text} watchlist!", color = 0x008000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return

@bot.tree.command(name = "wl_remove", description = "Remove an entry from your watchlist")
@app_commands.describe(choice = "Choose either 'steam' or 'stock'", index = "Where in the list is the item you want to remove located? (1-10)")
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def wl_remove(interaction: discord.Interaction, choice: app_commands.Choice[str], index: app_commands.Range[int, 1, 10]):

    await interaction.response.defer(ephemeral = False)

    chosen = choice.value

    if chosen == "steam":

        chosen_text = "Steam"

    else:

        chosen_text = "stocks"

    remove_resp = api("DELETE", "remove", {"for": chosen, "user": interaction.user.id, "index": index})

    remove_status = remove_resp["statusCode"]

    if remove_status == 403:

        embed = discord.Embed(title = "Error", description = f"Your {chosen_text} watchlist is empty!", color = 0xff0000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return

    elif remove_status == 400:

        embed = discord.Embed(title = "Error", description = f"{remove_resp['body'].split(': ')[1]}", color = 0xff0000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return
    
    else:

        embed = discord.Embed(title = "Error", description = f"'{json.loads(remove_resp['body'])['item']}' was successfully removed from your {chosen_text} watchlist!", color = 0x008000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return

@bot.tree.command(name = "wl", description = "Display your watchlist")
@app_commands.describe(choice = "Choose either 'steam', 'stock' or 'both'", index = "Which watchlist entry do you want to take a closer look at? (1-10)")
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def wl(interaction: discord.Interaction, choice: Optional[app_commands.Choice[str]] = "both", index: Optional[app_commands.Range[int, 1, 10]] = None):

    await interaction.response.defer(ephemeral = False)

    if choice != "both":

        chosen = choice.value

    else:

        chosen = choice

    if chosen == "steam":

        chosen_text = "Steam"

    else:

        chosen_text = "stocks"

    if choice == "both" and index != None:

        embed = discord.Embed(title = "Error", description = f"You cannot specify an index without specifying a watchlist type (steam/stock).", color = 0xff0000)

        await interaction.followup.send(embed = embed, ephemeral = False)

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

            message = f"Your {chosen_text} watchlist is empty!"

        embed = discord.Embed(title = "Error", description = message, color = 0xff0000)

        await interaction.followup.send(embed = embed, ephemeral = False)

        return

    elif get_status == 400:

        embed = discord.Embed(title = "Error", description = f"{get_resp['body'].split(': ')[1]}", color = 0xff0000)

        await interaction.followup.send(embed = embed, ephemeral = False)

        return

    # No error in request

    if retrieve == "specific":

        item = json.loads(get_resp["body"])
        item_name = item['item']

        embed, file = get_specific_item_embed(chosen, item_name)

        if file == "empty":

            await interaction.followup.send(embed = embed, ephemeral = False)
            return
        
        else:

            await interaction.followup.send(embed = embed, file = file, ephemeral = False)
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
        embed.add_field(name = "Stocks", value = f"{stock_prefix}{stock_list_string}", inline = True)

        await interaction.followup.send(embed = embed, ephemeral = False)
        return
    
    elif chosen == "steam":

        items = json.loads(get_resp["body"])

        embed = get_steam_embed(items)

        await interaction.followup.send(embed = embed, ephemeral = False)
        return

    else:

        items = json.loads(get_resp["body"])

        embed = get_stock_embed(items)

        await interaction.followup.send(embed = embed, ephemeral = False)
        return
    
@bot.tree.command(name = "search", description = "Search for a specific Steam item or stock.")
@app_commands.describe(choice = "Choose either 'steam' or 'stock'", name = "Steam: Exact name of item and wear (if any) at end in brackets | Stock: '[ticker]:[exchange]'")
@app_commands.choices(choice = [
    app_commands.Choice(name = "steam ", value = "steam"),
    app_commands.Choice(name = "stock ", value = "stock")
])
async def search(interaction: discord.Interaction, choice: app_commands.Choice[str], name: str):

    await interaction.response.defer(ephemeral = False)
    
    chosen = choice.value

    if chosen == "steam":

        chosen_text = "Steam item"

    else:

        chosen_text = chosen
        name = name.upper()

    valid = validate_name(chosen, name)

    if valid != 200:

        embed = discord.Embed(title = "Error", description = f"'{name}' is not a valid {chosen_text}!", color = 0xff0000)
        await interaction.followup.send(embed = embed, ephemeral = False)
        return

    # 'name' is validated

    embed, file = get_specific_item_embed(chosen, name)

    if file == "empty":

        await interaction.followup.send(embed = embed, ephemeral = False)
        return
    
    else:

        await interaction.followup.send(embed = embed, file = file, ephemeral = False)
        return

bot.run(TOKEN)