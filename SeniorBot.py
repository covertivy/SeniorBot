###########################################################################################
#                     _____            _             ______       _                       #
#                    /  ___|          (_)            | ___ \     | |                      #
#                    \ `--.  ___ _ __  _  ___  _ __  | |_/ / ___ | |_                     #
#                     `--. \/ _ \ '_ \| |/ _ \| '__| | ___ \/ _ \| __|                    #
#                    /\__/ /  __/ | | | | (_) | |    | |_/ / (_) | |_                     #
#                    \____/ \___|_| |_|_|\___/|_|    \____/ \___/ \__|                    #
#                                                                                         #
#                                 Creator: Raz Kissos                                     #
#                    GitHub page: https://github.com/RazKissos/SeniorBot                  #
###########################################################################################

from discord.ext.commands import Bot, CheckFailure, CommandError
from discord import Game, activity, Status
from discord.ext import commands
import configparser
import datetime
import discord
import json
import math
import asyncio
import requests
import random
import os

# Get Bot Data initialization class.
if os.path.exists('BotData.py'):
    import BotData 
else:
    raise Exception("BotData.py Does not exist!")


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__)) # Get relative path to our folder.
FRIEND_LIST_PATH = os.path.join(THIS_FOLDER, 'userfriends.json') # Create path of friendlist json. (name can be changed)
CONFIG_FILE_PATH = os.path.join(THIS_FOLDER, "botconfig.cfg") # Create path of config file. (name can be changed)
DATETIME_OBJ = datetime.datetime

BOT_DATA = BotData.BotData() # Our bot data object.

# Read\Create essential files
try:
    BOT_DATA.read_config_data(CONFIG_FILE_PATH)
    BOT_DATA.read_json(FRIEND_LIST_PATH) # Should not raise any exceptions but here just in case.
except Exception as e:
    print(f'{e}')
    exit()
    

# Create and Initialize Bot object.
BOT = Bot(command_prefix=BOT_DATA.BOT_PREFIX, description="Bot by Raz Kissos, helper and useful functions.") # Create the discord bot.
BOT.remove_command('help')


@BOT.event
async def on_ready():
    """[summary]
    this function sends a message in the console telling us the bot is up.
    it also configures the bot's status and sends the data to the servers.
    """
    BOT_DATA.BOT_NAME = BOT.user.name
    activity_info = activity.Activity(type=activity.ActivityType.listening, name= "{}help".format(BOT_DATA.BOT_PREFIX))
    await BOT.change_presence(activity=activity_info, status= BOT_DATA.STATUS)

def print_guilds():
    print("********************")
    print("Current servers: ")
    for server in BOT.guilds:
        print("- " + server.name)
    print("********************")

async def list_servers():
    """
    this function prints the connected server list every hour.
    """
    await BOT.wait_until_ready()
    while not BOT.is_closed():
        print_guilds()
        print("{}\nBot by Raz Kissos, helper and useful functions.\nFriend list json file path: {}\n********************\n".format(DATETIME_OBJ.today(), FRIEND_LIST_PATH))
        await asyncio.sleep(3600)

@BOT.event
async def on_command_error(ctx, error):
    """[summary]
    Excepts every error the bot receivs and prints it to the console.
    Args:
        ctx ([type]): the message context object.
        error ([type]): the excepted error. 
    """
    print("[!] ERROR: {}\n".format(error))


# Console not working for now.
async def console():
    await BOT.wait_until_ready()
    commands = [("help","shows this help message"), ("exit","closes the bot"), ("guilds", "prints the current guilds the bot is on"), 
                ("botinfo", "returns the bot's basic information")]
    while True:
        try:
            command = input(">").lower()
            
            if command == commands[0][0]: # help console command.
                print("Console commands:")
                for cmd in commands:
                    print("\t-" + cmd[0] + ": " + cmd[1] + ".")
            elif command == commands[1][0]: # exit console command.
                await BOT.close()
                return
            elif command == commands[2][0]: # guilds console command.
                print_guilds()
            elif command == commands[3][0]: # botinfo console command.
                print("********************")
                print("~BOT BY MARSE~\n-Prefix: {}\n-Token: {}\n-Friend List Path: {}".format(BOT_DATA.BOT_PREFIX, BOT_DATA.TOKEN, FRIEND_LIST_PATH))
                print("********************")
        except Exception as e:
            print(e)


# Create Asynchronous tasks for the bot before running:

asyncio.ensure_future(list_servers()) # Run the list_servers() function as an asynchronous coroutine.
# asyncio.ensure_future(console()) # Run the console as a coroutine. (Not Working for now)


###########################################################################################################################################################################
###############################################################| Server Dedicated Commands |###############################################################################
###########################################################################################################################################################################
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


@BOT.command(name='ban',
             description="Bans the tagged user and supplies a reason",
             pass_context=True
             )
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *,reason:str):
    if member in ctx.guild.members:
        await member.ban(reason=reason)
        await ctx.channel.send(f"Banned the user {member.mention} for reason: \"{reason}\"")
    else:
        await ctx.channel.send("User is not in the server!")
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure): # Check if the error was caused by missing permissions error.
        await ctx.channel.send("{} you are missing the required permissions to use this command!".format(ctx.message.author.mention))
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(name='unban',
             description="Unbans the tagged user and supplies a reason",
             pass_context=True
             )
@commands.has_permissions(ban_members=True)
async def unban(ctx, member:discord.User, *, reason:str):
    if member not in ctx.guild.members:
        await ctx.guild.unban(member)
        await ctx.channel.send(f"Unbanned the user {member.mention} with reason: \"{reason}\"")
    else:
        await ctx.channel.send("User is not banned!")
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CheckFailure): # Check if the error was caused by missing permissions error.
        await ctx.channel.send("{} you are missing the required permissions to use this command!".format(ctx.message.author.mention))
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(name='clean',
             description="Cleans a given amount of messages sent by the tagged user (If message amount is not specified automatically selects 100)",
             brief="Chat cleaner.",
             pass_context=True
             )
@commands.has_permissions(administrator=True)
async def clean(ctx, member:discord.Member, count:int=100):
    if count < 1:
        await ctx.channel.send("Zero or Negative amount of messages to delete was given!")
        return
    if len(ctx.message.mentions) != 1:
        await ctx.channel.send("Can only delete 1 user's messages at a time!")
        return
    
    iterator = ctx.channel.history()
    counter = 0
    msg_list = []
    while counter < count:
        try:
            msg = await iterator.next()
            if msg.author == member:
                msg_list.append(msg)
                counter += 1
        except:
            try:
                await ctx.channel.delete_messages(msg_list)
                print("Deleted {} messages from channel {}".format(counter, ctx.channel.name))
                return
            except:
                return
    try:
        await ctx.channel.delete_messages(msg_list)
        print("Deleted {} messages from channel {}".format(counter, ctx.channel.name))
    except:
        return
@clean.error
async def clean_error(ctx, error):
    if isinstance(error, CheckFailure): # Check if the error was caused by missing permissions error.
        await ctx.channel.send("{} Only Administrators can use this command!".format(ctx.message.author.mention))


@BOT.command(name="userinfo",
            description="Prints out the user's information in a nice embed",
            brief="{}whois @<tagged_member> | {}whois\n if no user is specified the selected user will be the sender".format(BOT_DATA.BOT_PREFIX,BOT_DATA.BOT_PREFIX),
            aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member: 
        member = ctx.message.author
    embed = discord.Embed(colour=discord.Colour(random.randint(1, 16777215)), timestamp=ctx.message.created_at,title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Name", value=member.name)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Nickname:", value=member.display_name)
    embed.add_field(name="Status", value=member.status)
    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M  UTC"))
    embed.add_field(name="Joined Server On:", value=(member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")))
    
    roles = [role.mention for role in member.roles[1:]]

    if len(member.roles[1:]) < 1:
        embed.add_field(name=f"Roles:",value="None", inline=False)
        embed.add_field(name="Highest Role:", value="None")
    elif roles != None:
        embed.add_field(name=f"Roles({len(roles)}):",value=",".join(roles), inline=False)
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
    
    await ctx.send(embed=embed)

###########################################################################################################################################################################
#################################################################| Fun and Useful Commands |###############################################################################
###########################################################################################################################################################################
@BOT.command(name='coinflip',
             description="Returns heads/tails.",
             brief="Excessicve coin flipper",
             aliases=['flip', 'coin']
             )
async def coinflip(ctx):
    await ctx.send(ctx.message.author.mention + " " + random.choice(['🧿Heads', '🧿Tails']))


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

    await ctx.send("1₿ = " + value + "💲")


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
    ~RandInt (<num1>,<num2>).\n For example ~RandInt <bottom limit> <top limit>.
    """
) # return a random integer between the numbers given.
async def RandInt(ctx, bottom:int, top:int):
    """[summary]
    Returns a random integer in a given range For example `~RandInt (10,20)`.
    the first parameter is the bottom range and the second is the top range.
    Args:
        ctx ([type]): the message context object.
        parameters (str): the range as a string for example (10,20).
    """
    if bottom < top:
        try:
            await ctx.send("Random integer between {} and {}: {}".format(bottom, top, random.randint(bottom, top)))
        except:
            await ctx.send("Invalid Parameters! check out {}help!".format(BOT_DATA.BOT_PREFIX))
    else:
        await ctx.send("Can not randomize a number with a min limit higher than the max limit!")


@BOT.command(
    name="Weather",
    aliases=["weather"],
    description="Displays the current weather in given coordinates.",
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

###########################################################################################################################################################################
##################################################################| Custom Friend Commands |###############################################################################
###########################################################################################################################################################################
@BOT.command(
    name="looking_to_play",
    aliases=["ltp", "play_with_me", "pwm"],
    description="Tags all your friends and dm's them asking to play",
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
    f.close()
    
    if str(ctx.author.id) not in data:
        await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")
    else:
        friends = data[str(ctx.author.id)] # get the list of the author's friends.
        all_usr_list = BOT.users # get all the users the bot has access to.
        list_of_mentions = list()
        for friend_id in friends: 
            for user in all_usr_list:
                if friend_id == str(user.id):
                    friend_obj = await BOT.fetch_user(int(friend_id))
                    list_of_mentions.append(friend_obj.mention)

                    if not friend_obj.dm_channel:
                        await friend_obj.create_dm()
                    
                    await friend_obj.send("Hi {}, {} wants to play {} with you!".format(friend_obj.mention, ctx.author.name, game))

        await ctx.channel.send("{} :\n{} is in need of your assistace! join him in his mighty {} game!".format(" ".join(list_of_mentions), ctx.author.mention, game))


@BOT.command(
    name="add_friend",
    description="Adds the tagged user to your list of friends, used with the 'looking to play' function",
    brief="""
    ~add_friend @Bob\n
    """,
    aliases=["add", "befriend"]
    )
async def add_friend(ctx):
    """[summary]
    Adds a user to your friend list which is used in the looking_to_play function.
    Args:
        ctx ([type]): the message context.
        user (discord.User): the tag of the user you wish to add. @BobbyBoy.

    Raises:
        Exception: if parameters are invalid.
    """
    if len(ctx.message.mentions) > 0:

        read_obj = open(FRIEND_LIST_PATH, "r")
        json_data = json.loads(read_obj.read())
        read_obj.close()

        if str(ctx.author.id) in json_data:
            for mention in ctx.message.mentions:
                if mention == ctx.message.author:
                    await ctx.send("You cannot add yourself as a friend! Go find some real ones...")
                else:
                    if str(mention.id) not in json_data[str(ctx.author.id)]:
                        json_data[str(ctx.author.id)].append(str(mention.id))
                        await ctx.channel.send(f"{mention.mention} added successfully!")
                    else:
                        await ctx.channel.send(f"{mention.mention} already in your friend list!")
        else:
            friend_list = list()
            for mention in ctx.message.mentions:
                if mention == ctx.message.author:
                    await ctx.send("You cannot add yourself as a friend! Go find some real ones...")
                else:
                    friend_list.append(str(mention.id))
                    await ctx.channel.send(f"{mention.mention} added successfully!")
            
            json_data.update({str(ctx.author.id):friend_list})

        write_obj = open(FRIEND_LIST_PATH, "w")
        write_obj.write(json.dumps(json_data))
        write_obj.close()
    else:
        await ctx.channel.send("Parameters invalid! check out {}help".format(BOT_DATA.BOT_PREFIX))


@BOT.command(
    name="remove_friend",
    aliases=["rmf", "unfriend"],
    description="removes an existing friend from your friend list.",
    brief="~rmf @Bob\n"
)
async def remove_friend(ctx):
    """[summary]
    Removes a friend from your friend list.
    Args:
        ctx ([type]): the message context object.
        user (discord.User): the mention of the user you want to remove.
    """
    if len(ctx.message.mentions) > 0:
        
        read_obj = open(FRIEND_LIST_PATH, "r")
        data = json.loads(read_obj.read())
        read_obj.close()
        
        if str(ctx.author.id) in data:
            for mention in ctx.message.mentions:
                if mention == ctx.message.author:
                    await ctx.send("Do you really hate yourself that much that you wish to unfriend yourself? pathetic.")
                else:
                    if str(mention.id) not in data[str(ctx.author.id)]:
                        await ctx.channel.send(f"{mention.mention} not in your friend list!")
                    else:
                        data[str(ctx.author.id)].remove(str(mention.id))
                        await ctx.channel.send(f"{mention.mention} removed successfully!")
        else:
            await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")

        write_obj = open(FRIEND_LIST_PATH, "w")
        write_obj.write(json.dumps(data))
        write_obj.close()

    else:
        await ctx.channel.send("invalid parameters! check out {}help!".format(BOT_DATA.BOT_PREFIX))


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
    read_obj.close()

    if (str(ctx.author.id) in data):
        if len(data[str(ctx.author.id)]) == 0:
            await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")
        else:
            embed = discord.Embed(color=discord.Color.dark_teal())
            embed.set_author(name="These are your current friends:")
            for friend_id in data[str(ctx.author.id)]:
                friend_obj = await BOT.fetch_user(friend_id)
                embed.add_field(name="--------------------", value="\t🔳" + friend_obj.mention, inline=False)
            await ctx.channel.send(ctx.author.mention, embed=embed)
    else:
        await ctx.channel.send("Too bad! seems you are lonely as fuck and do not have any friends!")

# Finally, Run the Bot!
BOT.run(BOT_DATA.TOKEN) # Run the bot.