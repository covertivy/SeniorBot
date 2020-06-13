# Creator: Raz Kissos.
# GitHub page: 'https://github.com/RazKissos/SeniorBot'.

from discord.ext.commands import Bot
from discord.ext import commands
from discord import Game
from discord import Status
from discord import activity
import configparser
import traceback
import datetime
import discord
import json
import math
import asyncio
import requests
import random
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__)) # Get relative path to our folder.
FRIEND_LIST_PATH = os.path.join(THIS_FOLDER, 'userfriends.json') # Create path of friendlist json. (name can be changed)
CONFIG_FILE_PATH = os.path.join(THIS_FOLDER, "botconfig.cfg") # Create path of config file. (name can be changed)
DATETIME_OBJ = datetime.datetime


class BotData:
    BOT_NAME = str()
    TOKEN = str()
    BOT_PREFIX = str()
    STATUS = Status.online

    def read_config_data(self, path: str):
        """[summary]
        Reads the bot config info from the config file and stores it in the BotData class.
        Args:
            path (str): path to config file
        """
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(path)
        self.BOT_PREFIX = cfg_parser['data']['prefix']
        self.TOKEN = cfg_parser['data']['token']
    
    def read_json(self, path:str):
        """[summary]
        Makes sure the friend list json file exists, if it doesn't exist the program will creat it itself.
        Args:
            path (str): path to friend list json file.
        """
        if not os.path.exists(path):
            creator = open(path, 'w+')
            creator.close()
        
        f = open(path, 'r') 
        f_str = f.read()
        if len(f_str) >= 2:
            if "{" != f_str[0] or "}" != f_str[-1]:
                writer = open(path, 'w')
                writer.write("{}")
                writer.close()
        else:
            writer = open(path, 'w')
            writer.write("{}")
            writer.close()

        f.close()


BOT_DATA = BotData() # Our bot data object.
BOT_DATA.read_config_data(CONFIG_FILE_PATH)
BOT_DATA.read_json(FRIEND_LIST_PATH)
BOT = Bot(command_prefix=BOT_DATA.BOT_PREFIX, description="Bot by Raz Kissos, helper and useful functions.") # Create the discord bot.
BOT.remove_command('help') # Remove default help command (we will replace it).


@BOT.event
async def on_ready():
    """[summary]
    this function sends a message in the console telling us the bot is up.
    it also configures the bot's status and sends the data to the servers.
    """
    BOT_DATA.BOT_NAME = BOT.user.name
    activity_info = activity.Activity(type=activity.ActivityType.listening, name= "~help")
    await BOT.change_presence(activity=activity_info, status= BOT_DATA.STATUS)


async def list_servers():
    """
    this function prints the connected server list every hour.
    """
    await BOT.wait_until_ready()
    while not BOT.is_closed():
        print("*****************")
        print("Current servers: ")
        for server in BOT.guilds:
            print("- " + server.name)
        print("*****************")
        print("{}\nBot by Marse, helper and useful functions.\nRunning bot {}\nFriend list json file path: {}\n********\n".format(DATETIME_OBJ.today(), BOT_DATA.BOT_NAME, FRIEND_LIST_PATH))
        await asyncio.sleep(3600)


@BOT.command(name="help",
            aliases=["h"],
            description="Shows this help message.")
async def help(ctx):
    """[summary]
    this function replaces the default help command from discord and sends a prettier and formatted help message.
    Args:
        ctx ([type]): the message context object.
    """
    author = ctx.message.author
    embed = discord.Embed(color=discord.Color.dark_teal())
    embed.set_author(name="Senior Bot's Commands:")
    for cmd in BOT.commands:
        embed.add_field(name= str("♿|~**" + cmd.name + "**: "), value=str(cmd.description + "\n👀|Aliases: " + str(cmd.aliases)), inline=False)
    await ctx.send(author.mention, embed=embed)


@BOT.command(name='8ball',
             description="Answers a yes/no question.",
             brief="Answers from the beyond...",
             aliases=['eight_ball', '8-ball', '8B']  # returns a random str for a deciding factor.
             )
async def eight_ball(ctx):
    """[summary]
    this function returns a random response to answer a question.
    the answer is picked in random frim a list of options.
    Args:
        ctx ([type]): the message context object.
    """
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely'
    ]
    await ctx.send(random.choice(possible_responses) + ', ' + ctx.message.author.mention)
    

@BOT.command(
        name="bitcoin",
        description="Returns the current market value of bitcoin.",
        aliases=["bc", "BC"]
    )  # returns the current bitcoin value in usd.
async def bitcoin(ctx):
    """[summary]
    this function grabs the bitcoin value json file from the bitcoin api
    and prints the USD value to the server.
    Args:
        ctx ([type]): the message context object.
    """
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']

    await ctx.send("Bitcoin Value is: " + value + " USD")


@BOT.command(
    name="CreateName",
    description="Creates a random name (format: <fname> <lname>)",
    brief= """Creates a random name (format: <fname> <lname>)\n
    (command format: <Command name> <Gender (f/m)>)""",
    aliases=["createname", "cn"]
) # returns a random name from an api.
async def CreateName(ctx, gender : str):
    """[summary]
    this function receivs a gender (f/m) and receivs a random name from the uinames api 
    according to the specified gender, creating a random name for the asker.
    Args:
        ctx ([type]): the message context object.
        gender (str): the gender of the generated name.
    """
    message = str()
    if gender == 'f':
        url = "https://uinames.com/api/?gender=female"
        response = requests.get(url)
        new_name = response.json()['name'] + ' ' + response.json()['surname']
        message = new_name
    elif gender == 'm':
        url = "https://uinames.com/api/?gender=male"
        response = requests.get(url)
        new_name = response.json()['name'] + ' ' + response.json()['surname']
        message = new_name
    else:
        message = "invalid parameters, (f/m) for an according name to the gender."
    await ctx.send(ctx.message.author.mention + message)


@BOT.command(
    name="RandInt",
    aliases=["RandI", "RInt", "RI"],
    description="Returns a random integer in a given range.",
    brief="""
    ~RandInt (<num1>,<num2>).\n For example ~RandInt (10,20).
    """
) # return a random integer between the numbers given.
async def RandInt(ctx, parameters:str):
    """[summary]
    Returns a random integer in a given range For example `~RandInt (10,20)`.
    the first parameter is the bottom range and the second is the top range.
    Args:
        ctx ([type]): the message context object.
        parameters (str): the range as a string for example (10,20).
    """
    values = parameters[1:-1].replace(' ', '')
    values = values.split(',')
    if int(values[0]) < int(values[1]):
        try:
            await ctx.send("Random integer between {} and {}: {}".format(values[0], values[1], random.randint(int(values[0]), int(values[1]))))
        except:
            await ctx.send("Invalid Parameters! check out {}help!".format(BOT_DATA.BOT_PREFIX))
    else:
        await ctx.send("Can not randomize a number with a min limit higher than the max limit!")


@BOT.command(
    name="Weather",
    aliases=["weather", "מזג-אויר"],
    description="Displays the current weather in kfar tavor.",
    brief="""
    ~Weather <lat>&<lon>. For example: ~Weather 62.3&46.9.
    """
) # returns the current weather in a certain coordination.
async def Weather(ctx, coords:str):
    """[summary]
    Asks this shitty weather api for the current weather in a certain coord.
    check out 'https://fcc-weather-api.glitch.me/' for more info on response format.
    Args:
        ctx ([type]): the message context object.
        coords (str): latitude and longitude parameters in the format "<lat>&<lon>" for example: "44.1213&12.65".
    """
    if '&' not in coords:
        await ctx.send("Message format wrong! check out ~help!")
    lat_lon = (float(coords.split('&')[0]), float(coords.split('&')[1]))
    url = "https://fcc-weather-api.glitch.me/api/current?lat={}&lon={}".format(lat_lon[0], lat_lon[1])
    response = json.loads(requests.get(url).content)
    weather_type = response["weather"][0]["main"] + " ({})".format( response["weather"][0]["description"])
    temp = str(response["main"]["temp"]) + "°"
    await ctx.send("The weather in {} today is {} and the temperature is {}.".format(coords, weather_type, temp))


@BOT.command(
    name="looking_to_play",
    aliases=["ltp", "play_with_me", "pwm"],
    description="Tags everyone and dm's them asking to play",
    brief="""
    ~looking_to_play <game_name>\n tags @everyone and also dm's your friends.
    """
)
async def looking_to_play(ctx, game: str):
    """[summary]
    Sends all your listed friends a request to play a given game.
    To add friends look for add_friend function.
    Args:
        ctx ([type]): the message context object.
        game (str): the game name you wish to play.
    """
    f = open(FRIEND_LIST_PATH, "r")
    data = json.loads(f.read()) # get the user friend data.
    if str(ctx.author.id) not in data:
        await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")
    else:
        friends = data[str(ctx.author.id)] # get the list of the author's friends.
        all_usr_list = BOT.users # get all the users the bot has access to.
        list_of_mentions = list()
        for friend_id in friends: 
            for user in all_usr_list:
                if friend_id == user.id:
                    friend_obj = await BOT.fetch_user(friend_id)
                    list_of_mentions.append(friend_obj.mention)

                    if not friend_obj.dm_channel:
                        friend_obj.create_dm
                    
                    await friend_obj.send("Hi {}, {} wants to play {} with you!".format(friend_obj.mention, ctx.author.name, game))

        await ctx.channel.send("{} \n{} is in need of your assistace! join him in his mighty {} game!".format(str(list_of_mentions)[1:-1], ctx.author.mention, game))

    f.close()


@BOT.command(
    name="add_friend",
    description="Adds the tagged user to your list of friends, used with the 'looking to play' function",
    brief="""
    ~add_friend @Bob\n
    """
    )
async def add_friend(ctx, user : discord.User):
    """[summary]
    Adds a user to your friend list which is used in the looking_to_play function.
    Args:
        ctx ([type]): the message context.
        user (discord.User): the tag of the user you wish to add. @BobbyBoy.

    Raises:
        Exception: if parameters are invalid.
    """
    if len(ctx.message.mentions) == 1:
        mentioned_user = user.id
        read_obj = open(FRIEND_LIST_PATH, "r")

        data = json.loads(read_obj.read())
        if str(ctx.author.id) in data:
            if user.id not in data[str(ctx.author.id)]:
                data[str(ctx.author.id)].append(user.id)
                await ctx.channel.send("Friend added successfully!")
            else:
                await ctx.channel.send("User already in your friend list!")
        else:
            friend_list = list()
            friend_list.append(user.id)
            data.update({str(ctx.author.id):friend_list})

        write_obj = open(FRIEND_LIST_PATH, "w")
        write_obj.write(json.dumps(data))
        read_obj.close()
        write_obj.close()
    else:
        await ctx.channel.send("Parameters invalid! check out {}help".format(BOT_DATA.BOT_PREFIX))


@BOT.command(
    name="remove_friend",
    aliases=["rmf", "unfriend"],
    description="removes an existing friend from your friend list.",
    brief="~rmf @Bob\n"
)
async def remove_friend(ctx, user : discord.User):
    """[summary]
    Removes a friend from your friend list.
    Args:
        ctx ([type]): the message context object.
        user (discord.User): the mention of the user you want to remove.
    """
    if len(ctx.message.mentions) == 1:
        mentioned_user = user.id
        read_obj = open(FRIEND_LIST_PATH, "r")

        data = json.loads(read_obj.read())
        if str(ctx.author.id) in data:
            if user.id not in data[str(ctx.author.id)]:
                await ctx.channel.send("User not in your friend list!")
            else:
                data[str(ctx.author.id)].remove(mentioned_user)
                await ctx.channel.send("Friend removed successfully!")
        else:
            await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")

        write_obj = open(FRIEND_LIST_PATH, "w")
        write_obj.write(json.dumps(data))
    else:
        await ctx.channel.send("invalid parameters! check out {}help!".format(BOT_DATA.BOT_PREFIX))
    
    read_obj.close()
    write_obj.close()


@BOT.command(
    name="my_friends",
    aliases=["friends", "friend_list"],
    description="prints the mention of all existing friends from your friends list.",
    brief="~my_friends\n"
)
async def my_friends(ctx):
    """[summary]
    Prints a list of mentions of the users in you friend list.
    Args:
        ctx ([type]): the message context object.
    """
    read_obj = open(FRIEND_LIST_PATH, "r")
    data = json.loads(read_obj.read())
    if (str(ctx.author.id) in data):
        if len(data[str(ctx.author.id)]) == 0:
            await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")
        else:
            embed = discord.Embed(color=discord.Color.dark_teal())
            embed.set_author(name="These are your current friends:")
            for friend in data[str(ctx.author.id)]:
                friend_obj = await BOT.fetch_user(friend)
                embed.add_field(name="--------------------", value="\t🔳" + friend_obj.mention, inline=False)
            await ctx.channel.send(ctx.author.mention, embed=embed)
    else:
        await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")


@BOT.event
async def on_command_error(ctx, error):
    """[summary]
    Excepts every error the bot receivs and prints it to the console.
    Args:
        ctx ([type]): the message context object.
        error ([type]): the excepted error. 
    """
    print("""----------/\\/\\/\\/\\/\\/\\/\\/\\/\\----------\n~ ERROR: {}\n----------\\/\\/\\/\\/\\/\\/\\/\\/\\/----------""".format(error))


BOT.loop.create_task(list_servers()) # Run the list_servers() function as an asynchronous coroutine.
BOT.run(BOT_DATA.TOKEN) # Run the bot.
