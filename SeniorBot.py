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
from discord.ext import commands
from discord import activity
import discord
import datetime
import asyncio
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

# Read essential files.
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
BOT.remove_command("help")  # Remove default help command (will replace later).


@BOT.event
async def on_ready():
    """
    This function sends a message in the console telling us the bot is up.
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
    This function prints the bot's connected server list every hour.
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
    print("Bot is closing...")
    await asyncio.sleep(1)


@BOT.event
async def on_command_error(ctx, error):
    """
    Excepts every error the bot receivs and prints it to the console.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        error (from discord.errors): the excepted error.
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
    This command replaces the default help command from discord and sends a prettier and formatted help message.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        command_name (str): the command name to get data about (optional).
    """

    if command_name is None:  # Check if help was invoked as a specific command help.
        # Create return embed
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
        await ctx.send(
            embed=embed
        )  # Send the shallow info of each command as an embed.
    else:  # Help command was invoked as a specific command help.
        # Check if command name is actually a command.
        if command_name in [command.name for command in BOT.commands]:
            # Get the requested command object.
            cmd_to_print = None
            for cmd in BOT.commands:
                if cmd.name == command_name:
                    cmd_to_print = cmd
                    break

            # Check if command has any aliases, if not return 'None'.
            if len(cmd_to_print.aliases) == 0:
                aliases_str = "None"
            else:
                aliases_str = ", ".join(
                    [f'"{alias}"' for alias in cmd_to_print.aliases]
                )

            # Create and send the thorough command info embed.
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
        else:  # Command name was not found in the bot's commands.
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
    """
    This command will apply a server mute to the given member and send an embedded message to confirm the mute.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        member (discord.Member): the member to be muted object.
    """
    # Check if member is in the guild.
    guild_member = await ctx.guild.fetch_member(member.id)
    if member == guild_member:
        await member.edit(mute=True)  # Apply server mute.
        embed = discord.Embed(
            title="User Muted!",
            description=f"**{member}** was muted by **{ctx.message.author}**!",
            color=discord.Color.red(),
        )
        await ctx.channel.send(embed=embed)  # Send fancy mute embed.


@mute.error
async def mute_error(ctx, error):
    if isinstance(
        error, MissingPermissions
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help mute' to see more information."
        )
    elif isinstance(
        error, discord.HTTPException
    ):  # Check if error was caused because member fetch had failed.
        await ctx.channel.send(f"Member is not in the server!")
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
    """
    This command unmutes the server mute that was put on the given member.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        member (discord.Member): the member to be unmuted object.
    """
    # Check if member is in the guild.
    guild_member = await ctx.guild.fetch_member(member.id)
    if member == guild_member:
        await member.edit(mute=False)  # Apply server unmute.
        embed = discord.Embed(
            title="User Unmuted!",
            description=f"**{member}** was unmuted by **{ctx.message.author}**!",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)  # Send fancy mute embed.


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(
        error, MissingPermissions
    ):  # Check if the error was caused by missing permissions error.
        await ctx.channel.send(
            f"{ctx.message.author.mention} you are missing the required permissions to use this command!\nplease use '{BOT_DATA.BOT_PREFIX}help unmute' to see more information."
        )
    elif isinstance(
        error, discord.HTTPException
    ):  # Check if error was caused because member fetch had failed.
        await ctx.channel.send(f"Member is not in the server!")
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
    """
    This command checks if the given user is indeed a member of the current server, if so it kicks him and sends him the reason.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        member (discord.Member): the member to be kicked.
        reason (str): the reason for the kick.
    """
    # Get the member from the guild, if returned None then member is not in the guild.
    guild_member = await ctx.guild.fetch_member(member.id)
    if guild_member is not None:  # Member exists, need to kick.
        await guild_member.kick(reason=reason)
        await ctx.channel.send(
            f'Kicked the member {guild_member.mention} for reason "{reason}"'
        )
    else:  # Member not in the server.
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
    """
    This command checks if the given user is indeed a member of the current server, if so it bans him and sends him the reason.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        member (discord.Member): the member to be banned.
        reason (str): the reason for the ban.
    """
    # Get the member from the guild, if returned None then member is not in the guild.
    guild_member = await ctx.guild.fetch_member(member.id)
    if guild_member is not None:  # Member exists, need to ban.
        await guild_member.ban(reason=reason)
        await ctx.channel.send(
            f'Banned the member {guild_member.mention} for reason: "{reason}"'
        )
    else:  # Member not in the server.
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
    brief="Unbans the named user from the server.",
    description="Unbans the named user from the server.\n**Important** - user must have the ***ban members*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}unban <banned user's name>** -> unbans the user with the corresponding name from the server (user has to be banned).",
    pass_context=True,
)
@commands.has_permissions(ban_members=True)
async def unban(ctx, name_of_user: str):
    """
    This command checks if the given username belongs to a banned member of the current server, if so it unbans him.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        name_of_user (str): the username of the member to be unbanned.
    """
    guild_bans = await ctx.guild.bans()  # Get all the guild bans.
    banned_users = [ban.user for ban in guild_bans]  # Create a list of banned users.

    for user in banned_users:  # Find the user to unban and unban him.
        if user.name == name_of_user:
            await ctx.guild.unban(user)
            await ctx.channel.send(f"Unbanned the user {user.mention}!")
            return

    # Will occure only when user is not banned since we return if he is.
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
    description="Cleans the given amount of messages that were sent by the mentioned member (If message amount is not specified automatically selects 10).\n**Important** - user must have the ***administrator*** permission.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}clean @<user mention> <message amount>** -> deletes the given amount of messages the mentioned member has has sent in the current text channel (message amount is optional, default will be 10).",
    pass_context=True,
)
@commands.has_permissions(administrator=True)
async def clean(ctx, member: discord.Member, count: int = 10):
    """
    This command receives a member object and a count (optional), then checks if the member is in the server and if the count is positive.
    If all the checks are passed, The member's messages are stored in a list and then asynchronously deleted.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        member (discord.Member): the member of whom the messages will be deleted.
        count (int, optional): the amount of messages to be deleted. Defaults to 10.
    """
    # Perform checks to see if the command can indeed be run in the current context.
    guild_member = await ctx.guild.fetch_member(member.id)
    if guild_member is None:  # Check if member is in the guild.
        await ctx.channel.send("Given member is not a member of this server.")
        return
    if count < 1:  # Check if the message amount to delete is not valid (not positive).
        await ctx.channel.send(
            "Zero or Negative amount of messages to delete was given!"
        )
        return
    if len(ctx.message.mentions) != 1:  # Check if more than 1 member was mentioned.
        await ctx.channel.send("Can only delete 1 user's messages at a time!")
        return

    # Create the channel messages iterator.
    iterator = ctx.channel.history()
    counter = 0
    msg_list = []
    while counter < count:
        try:
            msg = await iterator.next()
            if msg.author == member:
                msg_list.append(msg)  # Get a user's message and store it.
                counter += 1  # Update the counter.
        except:
            try:
                await ctx.channel.delete_messages(
                    msg_list
                )  # Run asynchronous coroutine delete_messages to delete all the found messages from the user.
                print(
                    f"Deleted {counter} messages from channel {ctx.channel.name}"
                )  # Log the event.
                return
            except:
                return
    try:
        # Run asynchronous coroutine delete_messages to delete all the found messages from the user after reached counter.
        await ctx.channel.delete_messages(msg_list)
        print(
            f"Deleted {counter} messages from channel {ctx.channel.name}"
        )  # Log the event.
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
    """
    This command sends an embed to the context's channel which will contain general server information.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
    """
    guild = ctx.guild  # Get the guild object
    # Create the embed.
    embed_ret = discord.Embed(colour=discord.Color.gold())
    embed_ret.set_thumbnail(url=guild.icon_url)
    embed_ret.set_footer(text="Server Information")
    embed_ret.add_field(name="Server Name", value=guild.name)
    embed_ret.add_field(
        name="🧍Memeber Count🧍", value=str(guild.member_count), inline=False
    )
    invite_url = await ctx.channel.create_invite(max_age=3600, max_uses=3, unique=False)
    embed_ret.add_field(name="🔗Invite Link🔗", value=invite_url, inline=False)
    await ctx.channel.send(embed=embed_ret)  # Send the embed.


@BOT.command(
    name="userinfo",
    aliases=["whois"],
    brief="Shows the mentioned member information.",
    description="Sends an embed containing the mentioned member's information (icon, name, roles, nickname, id, etc...).\nIf no member was mentioned the command will show the info of the author.",
    usage=f"| **{BOT_DATA.BOT_PREFIX}userinfo @<mentioned_member>** -> will show the mentioned member's general information.\n| **{BOT_DATA.BOT_PREFIX}userinfo** -> will show the author's general information.",
)
async def userinfo(ctx, member: discord.Member = None):
    """
    This command will optionally receive an member object and will return an embedded message containing all the info about the member.
    If the member object is None then the command will return the author's information instead.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        member (discord.Member, optional): the member object of whom's information will be displayed. Defaults to None. if is None then author's
            info will be displayed instead.
    """
    if member is None:  # Check if member was give, if not choose the author.
        member = ctx.message.author

    # Create the embedded message and add info.
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

    await ctx.send(embed=embed)  # Send the embedded message.


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
    """
    This command returns a random response (head / tails) to simulate a coin toss.
    Args:
        ctx (discord.ext.commands.Context): the command context object.
    """
    await ctx.send(
        ctx.message.author.mention + " " + random.choice(["🧿Heads", "🧿Tails"])
    )  # Return the random response.


@BOT.command(
    name="RandInt",
    aliases=["RandI", "RInt", "RI"],
    brief="Returns a random integer in a given range.",
    description="Returns a random integer in a given range. The range is between (bottom limit) up to (top limit).",
    usage=f"| **{BOT_DATA.BOT_PREFIX}RandInt <bottom limit> <top limit>** -> will return a random number between bottom limit and top limit (top limit is in range).",
)
async def RandInt(ctx, bottom: int, top: int):
    """
    This command will return a random integer in the range of (bottom ; top + 1).
    Args:
        ctx (discord.ext.commands.Context): the command context object.
        bottom (int): bottom range limit.
        top (int): top range limit.
    """
    if bottom < top:  # Check if input is valid (top > bottom)
        try:
            await ctx.send(
                "Random integer between {} and {}: {}".format(
                    bottom, top, random.randint(bottom, top)
                )  # Return random integer.
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
