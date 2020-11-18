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
if os.path.exists("BotData.py"):
    import BotData
else:
    raise Exception("BotData.py Does not exist!")


THIS_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)  # Get relative path to our folder.
CONFIG_FILE_PATH = os.path.join(
    THIS_FOLDER, "botconfig.cfg"
)  # Create path of config file. (name can be changed)
DATETIME_OBJ = datetime.datetime

BOT_DATA = BotData.BotData()  # Our bot data object.

# Read\Create essential files
try:
    BOT_DATA.read_config_data(CONFIG_FILE_PATH)
except Exception as e:
    print(f"{e}")
    exit()


# Create and Initialize Bot object.
BOT = Bot(
    command_prefix=BOT_DATA.BOT_PREFIX,
    description="Bot by Raz Kissos, helper and useful functions.",
)  # Create the discord bot.
BOT.remove_command("help")


@BOT.event
async def on_ready():
    """[summary]
    this function sends a message in the console telling us the bot is up.
    it also configures the bot's status and sends the data to the servers.
    """
    BOT_DATA.BOT_NAME = BOT.user.name
    activity_info = activity.Activity(
        type=activity.ActivityType.listening, name="{}help".format(BOT_DATA.BOT_PREFIX)
    )
    await BOT.change_presence(activity=activity_info, status=BOT_DATA.STATUS)


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
        print(
            "{}\nBot by Raz Kissos, helper and useful functions.\n********************\n".format(
                DATETIME_OBJ.today()
            )
        )
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


# Create Asynchronous tasks for the bot before running:

asyncio.ensure_future(
    list_servers()
)  # Run the list_servers() function as an asynchronous coroutine.


###########################################################################################################################################################################
###############################################################| Server Dedicated Commands |###############################################################################
###########################################################################################################################################################################
@BOT.command(name="help", aliases=["h"], description="Shows this help message.")
async def help(ctx):
    """[summary]
    this function replaces the default help command from discord and sends a prettier and formatted help message.
    Args:
        ctx ([type]): the message context object.
    """
    author = ctx.message.author
    embed = discord.Embed(color=discord.Color.gold())
    embed.set_thumbnail(url=BOT.user.avatar_url)
    embed.set_footer(text="Senior Bot's Commands")
    for cmd in BOT.commands:
        embed.add_field(
            name=str("♿|~**" + cmd.name + "**: "),
            value=str(cmd.description + "\n👀|Aliases: " + str(cmd.aliases)),
            inline=False,
        )
    await ctx.send(embed=embed)


@BOT.command(
    name="kick",
    description="Kicks the tagged user and supplies a reason",
    pass_context=True,
)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str):
    if member in ctx.guild.members:
        await member.kick(reason=reason)
        await ctx.channel.send(
            f'Kicked the member {member.mention} for reason "{reason}"'
        )
    else:
        await ctx.channel.send("User is not in the server")


@kick.error
async def kick_error(ctx, error):
    if isinstance(
        error, commands.CheckFailure
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            "{} you are missing the required permissions to use this command!".format(
                ctx.message.author.mention
            )
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="ban",
    description="Bans the tagged user and supplies a reason",
    pass_context=True,
)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str):
    if member in ctx.guild.members:
        await member.ban(reason=reason)
        await ctx.channel.send(
            f'Banned the member {member.mention} for reason: "{reason}"'
        )
    else:
        await ctx.channel.send("User is not in the server!")


@ban.error
async def ban_error(ctx, error):
    if isinstance(
        error, commands.CheckFailure
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            "{} you are missing the required permissions to use this command!".format(
                ctx.message.author.mention
            )
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="unban",
    description="Unbans the tagged user and supplies a reason",
    pass_context=True,
)
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: discord.User, *, reason: str):
    if member not in ctx.guild.members:
        await ctx.guild.unban(member)
        await ctx.channel.send(
            f'Unbanned the user {member.mention} with reason: "{reason}"'
        )
    else:
        await ctx.channel.send("User is not banned!")


@unban.error
async def unban_error(ctx, error):
    if isinstance(
        error, commands.CheckFailure
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            "{} you are missing the required permissions to use this command!".format(
                ctx.message.author.mention
            )
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="clean",
    description="Cleans a given amount of messages sent by the tagged user (If message amount is not specified automatically selects 100)",
    brief="Chat cleaner.",
    pass_context=True,
)
@commands.has_permissions(administrator=True)
async def clean(ctx, member: discord.Member, count: int = 100):
    if count < 1:
        await ctx.channel.send(
            "Zero or Negative amount of messages to delete was given!"
        )
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
                print(
                    "Deleted {} messages from channel {}".format(
                        counter, ctx.channel.name
                    )
                )
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
    if isinstance(
        error, CheckFailure
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            "{} Only Administrators can use this command!".format(
                ctx.message.author.mention
            )
        )


@BOT.command(
    name="serverinfo", aliases=["info"], description="Shows the server information"
)
async def information(ctx):
    guild = ctx.guild
    embed_ret = discord.Embed(colour=discord.Color.gold())
    embed_ret.set_thumbnail(url=guild.icon_url)
    embed_ret.set_footer(text="Server Information")
    embed_ret.add_field(name="Server Name", value=guild.name)
    embed_ret.add_field(
        name="🧍Memeber Count🧍", value=str(guild.member_count), inline=False
    )
    invite_url = await ctx.channel.create_invite(max_age=3600, max_uses=3, unique=False)
    embed_ret.add_field(name="🔗Invite Link🔗", value=invite_url, inline=False)
    await ctx.channel.send(embed=embed_ret)


@BOT.command(
    name="userinfo",
    description="Prints out the user's information in a nice embed",
    brief="{}whois @<tagged_member> | {}whois\n if no user is specified the selected user will be the sender".format(
        BOT_DATA.BOT_PREFIX, BOT_DATA.BOT_PREFIX
    ),
    aliases=["whois"],
)
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour(random.randint(1, 16777215)),
        timestamp=ctx.message.created_at,
        title=f"User Info - {member}",
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Name", value=member.name)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Nickname:", value=member.display_name)
    embed.add_field(name="Status", value=member.status)
    embed.add_field(
        name="Created Account On:",
        value=member.created_at.strftime("%a, %#d %B %Y, %I:%M  UTC"),
    )
    embed.add_field(
        name="Joined Server On:",
        value=(member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")),
    )

    roles = [role.mention for role in member.roles[1:]]

    if len(member.roles[1:]) < 1:
        embed.add_field(name=f"Roles:", value="None", inline=False)
        embed.add_field(name="Highest Role:", value="None")
    elif roles != None:
        embed.add_field(
            name=f"Roles({len(roles)}):", value=",".join(roles), inline=False
        )
        embed.add_field(name="Highest Role:", value=member.top_role.mention)

    await ctx.send(embed=embed)


###########################################################################################################################################################################
#################################################################| Fun and Useful Commands |###############################################################################
###########################################################################################################################################################################
@BOT.command(
    name="coinflip",
    description="Returns heads/tails.",
    brief="Excessicve coin flipper",
    aliases=["flip", "coin"],
)
async def coinflip(ctx):
    await ctx.send(
        ctx.message.author.mention + " " + random.choice(["🧿Heads", "🧿Tails"])
    )


@BOT.command(
    name="RandInt",
    aliases=["RandI", "RInt", "RI"],
    description="Returns a random integer in a given range.",
    brief="""
    ~RandInt (<num1>,<num2>).\n For example ~RandInt <bottom limit> <top limit>.
    """,
)  # return a random integer between the numbers given.
async def RandInt(ctx, bottom: int, top: int):
    """[summary]
    Returns a random integer in a given range For example `~RandInt (10,20)`.
    the first parameter is the bottom range and the second is the top range.
    Args:
        ctx ([type]): the message context object.
        parameters (str): the range as a string for example (10,20).
    """
    if bottom < top:
        try:
            await ctx.send(
                "Random integer between {} and {}: {}".format(
                    bottom, top, random.randint(bottom, top)
                )
            )
        except:
            await ctx.send(
                "Invalid Parameters! check out {}help!".format(BOT_DATA.BOT_PREFIX)
            )
    else:
        await ctx.send(
            "Can not randomize a number with a min limit higher than the max limit!"
        )


# Finally, Run the Bot!
BOT.run(BOT_DATA.TOKEN)  # Run the bot.
