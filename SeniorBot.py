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

from discord.ext.commands import *
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
    """
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
    """
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
@BOT.command(
    name="help",
    aliases=["h"],
    brief="Shows the help message.\nAlso can be used as a single command help message.",
    description="When sent with no arguments, the command simply prints out all the command names and their brief explanations. But when sending a command name as an argument the command will print out a full list of the command's fields.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}help** -> print out the full list of commands.\n| **{BOT_DATA.BOT_PREFIX}help <command name>** - > print out thorough description of the command with the matching name",
)
async def help(ctx, command_name: str = None):
    """
    this function replaces the default help command from discord and sends a prettier and formatted help message.
    Args:
        ctx ([type]): the message context object.
        command
    """
    if command_name is None:
        author = ctx.message.author
        embed = discord.Embed(color=discord.Color.gold())
        embed.set_thumbnail(url=BOT.user.avatar_url)
        embed.set_footer(text="Senior Bot's Commands")

        for cmd in BOT.commands:
            embed.add_field(
                name=str(f"♿|**{BOT_DATA.BOT_PREFIX}{cmd.name}**: "),
                value=str(f"❓ {cmd.brief}"),
                inline=False,
            )
        await ctx.send(embed=embed)
    else:
        if command_name in [command.name for command in BOT.commands]:
            cmd_to_print = None
            for cmd in BOT.commands:
                if cmd_to_print is not None:
                    break
                elif cmd.name == command_name:
                    cmd_to_print = cmd

            if len(cmd_to_print.aliases) == 0:
                aliases_str = "None"
            else:
                aliases_str = ", ".join(
                    [f'"{alias}"' for alias in cmd_to_print.aliases]
                )

            embed = discord.Embed(color=discord.Color.dark_orange())
            embed.set_footer(text=f'"{cmd_to_print.name}" thorough description')
            embed.add_field(
                name="💬 Command Name 💬", value=cmd_to_print.name, inline=False
            )
            embed.add_field(
                name="❓ Brief Explanation ❓", value=cmd_to_print.brief, inline=False
            )
            embed.add_field(
                name="📰 Description 📰", value=cmd_to_print.description, inline=False
            )
            embed.add_field(
                name="⚙ Command Usage ⚙", value=cmd_to_print.usage, inline=False
            )
            embed.add_field(
                name="🎭 Command Name Aliases 🎭", value=aliases_str, inline=False
            )
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f"No command named {command} was found!")


@BOT.command(
    name="mute",
    brief="Mutes the mentioned member.",
    description="Mutes the mentioned member by giving him a server mute.\n**Important** - user must have the ***administrator*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}mute @<member mention>** -> will apply a server mute to the mentioned member.",
    pass_context=True,
)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    guild_member = await ctx.guild.fetch_member(member.id)
    if member == guild_member:
        await member.edit(mute=True)
        embed = discord.Embed(
            title="User Muted!",
            description=f"**{member}** was muted by **{ctx.message.author}**!",
            color=discord.Color.red(),
        )
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send(f"Member {member.mention} is not in the server!")


@mute.error
async def mute_error(ctx, error):
    if isinstance(
        error, MissingPermissions
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help mute' to see more information."
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="unmute",
    brief="Unmutes the mentioned member.",
    description="Unmutes the mentioned member by removing his server mute.\n**Important** - user must have the ***administrator*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}unmute @<member mention>** -> will remove the server mute from the mentioned member.",
    pass_context=True,
)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    guild_member = await ctx.guild.fetch_member(member.id)
    if member == guild_member:
        await member.edit(mute=False)
        embed = discord.Embed(
            title="User Unmuted!",
            description=f"**{member}** was unmuted by **{ctx.message.author}**!",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
    else:
        await ctx.channel.send(f"Member {member.mention} is not in the server!")


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(
        error, MissingPermissions
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help unmute' to see more information."
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="kick",
    brief="Kicks the mentioned member with a reason.",
    description="Kicks the mentioned member and sends the reason given by the admin.\n**Important** - user must have the ***kick members*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}kick @<member mention> <reason>** -> kicks the mentioned member and sends the reason to him (reason does not have to be in quotes).",
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
        error, MissingPermissions
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help kick' to see more information."
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="ban",
    brief="Bans the mentioned member with a reason.",
    description="Bans the mentioned member and sends the reason given by the admin.\n**Important** - user must have the ***ban members*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}ban @<member mention> <reason>** -> bans the mentioned member and sends the reason to him (reason does not have to be in quotes).",
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
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help ban' to see more information."
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="unban",
    brief="Unbans the mentioned user from the server.",
    description="Unbans the mentioned user from the server.\n**Important** - user must have the ***ban members*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}unban @<user mention>** -> unbans the mentioned user from the server (user has to be banned).",
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
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help unban' to see more information."
        )
    else:
        await ctx.channel.send(f"Error! {error}")


@BOT.command(
    name="clean",
    brief="Cleans a given number of a user's messages from the text channel.",
    description="Cleans the given amount of messages that were sent by the mentioned member (If message amount is not specified automatically selects 100).\n**Important** - user must have the ***administrator*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}clean @<user mention> <message amount>** -> deletes the given amount of messages the mentioned member has has sent in the current text channel (message amount is optional, default will be 100).",
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
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help clean' to see more information."
        )


@BOT.command(
    name="serverinfo",
    aliases=["info"],
    brief="Shows server information.",
    description="Shows the all the server information (icon, memeber count, etc...).",
    usage=f"| **{BOT_DATA.BOT_PREFIX}serverinfo** -> will print an embed with the general server information.",
)
async def serverinfo(ctx):
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
    aliases=["whois"],
    brief="Shows the mentioned member information.",
    description="Sends an embed containing the mentioned member's information (icon, name, roles, nickname, id, etc...).\nIf no member was mentioned the command will show the info of the author.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}userinfo @<mentioned_member>** -> will show the mentioned member's general information.\n| **{BOT_DATA.BOT_PREFIX}userinfo** -> will show the author's general information.",
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
    aliases=["flip", "coin"],
    brief="Returns heads/tails.",
    description="This command simulates a coinflip by choosing randomly heads or tails.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}coinflip** -> will print out a random response which would be either 'heads' or 'tails'.",
)
async def coinflip(ctx):
    await ctx.send(
        ctx.message.author.mention + " " + random.choice(["🧿Heads", "🧿Tails"])
    )


@BOT.command(
    name="RandInt",
    aliases=["RandI", "RInt", "RI"],
    brief="Returns a random integer in a given range.",
    description="Returns a random integer in a given range. The range is between (bottom limit) up to (top limit).",
    usage=f"| **{BOT_DATA.BOT_PREFIX}RandInt <bottom limit> <top limit>** -> will return a random number between bottom limit and top limit (top limit is in range).",
)
async def RandInt(ctx, bottom: int, top: int):
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
