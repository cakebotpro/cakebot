"""
    Cakebot - A cake themed Discord bot
    Copyright (C) 2019-current year  Reece Dunham

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord
from sys import exit as _exit, argv
from os import getenv
from logging import getLogger
from filehandlers import AbstractFile, FileManipulator
from github import Github
from area4 import divider
from fbootstrap import bootstrap
from reverse_geocoder import search
from discord.utils import oauth_url
from slots import row, result
from iss import Imp as ISSimp
from factdata import FactImp
from club.cakebot import (
    TextCommandsUtil,
    EmbedUtil,
    UserUtil,
    Preconditions,
    GitHubUtil,
    BotUtil,
    Database,
)
from discord_sentry_reporting import use_sentry
from datetime import datetime
from sentry_sdk import configure_scope
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

logger = getLogger("cakebot")
logger.setLevel(10)

config = None
if getenv("TEST_ENV") != "yes":
    config = FileManipulator(AbstractFile("config.json")).load_from_json()
AbstractFile("servers.txt").touch()
servers = FileManipulator(AbstractFile("servers.txt"))

g = None
try:
    g = Github(config["tokens"]["github"])  # type: ignore
except (KeyError, TypeError):
    logger.warning("GitHub credentials not found, skipping...")

wordsapi_token = None
try:
    wordsapi_token = config["tokens"]["wordsapi"]  # type: ignore
except (KeyError, TypeError):
    logger.warning("WordsAPI credentials not found, skipping...")

client = discord.AutoShardedClient()

if getenv("PRODUCTION") is not None:
    use_sentry(
        client,
        dsn="https://e735b10eff2046538ee5a4430c5d2aca@sentry.io/1881155",
        debug=True,
        integrations=[AioHttpIntegration(), SqlalchemyIntegration()],
    )
    logger.debug("Loaded Sentry!")


if "shell" in argv:
    from ptpython.repl import embed

    embed(globals(), locals())
    exit()


def update_servers():
    bootstrap(client, servers)
    servers.refresh()


@client.event
async def on_ready():
    update_servers()
    if getenv("PRODUCTION") is not None:
        await client.change_presence(
            activity=discord.Game(name=config["status"])
        )
    else:
        await client.change_presence(
            activity=discord.Game(name="Running development build")
        )
    logger.info(
        "Ready to roll, I'll see you on Discord: @" + str(client.user)
    )


@client.event
async def on_message(message):
    Bot_Prefix = "+"
    if getenv("PRODUCTION") is None:
        Bot_Prefix = "-"

    if not message.content.startswith(Bot_Prefix):
        return

    with configure_scope() as scope:
        # show username of discord user in sentry
        scope.user = {
            "id": message.author.id,
            "username": str(message.author),
        }

    # Split input
    args = message.content[len(Bot_Prefix) :].split()

    cmd = args[0].lower()

    # the arg array ex. ["hello", "world"]
    args = args[1:]

    s = message.channel.send

    if (
        cmd == "8"
        or cmd == "report"
        or cmd == "define"
        or cmd == "stars"
        or cmd == "homepage"
        or cmd == "clapify"
        or cmd == "cookie"
    ) and Preconditions.checkArgsAreNotNull(args):
        return await s(
            embed=EmbedUtil.prep(
                "That command expected an argument (or arguments), but you didn't give it any!",
                "[Read the docs?](https://cakebot.club/commands.html)",
            )
        )

    tcu_result = TextCommandsUtil.handle_common_commands(message, args, cmd)
    if tcu_result is not None:
        return await s(tcu_result)

    if cmd == "help":
        return await s(
            embed=EmbedUtil.prep(
                title="Help",
                description="You can check out [this page of our website](https://cakebot.club/commands/) for a full command list!",
            )
        )

    elif cmd == "ping":
        return await s(f"🏓 - websocket responded in {client.latency}")

    elif cmd == "invite":
        return await s(
            embed=EmbedUtil.prep(
                "Invite Cakebot",
                f"[Click here to invite me!]({oauth_url(580573141898887199, permissions=discord.Permissions.all())})",
            )
        )

    elif cmd == "joke":
        return await s(
            embed=EmbedUtil.prep(
                f'**{TextCommandsUtil.common("jokes")}**',
                f"{divider(7)}{divider(7)}",
            )
        )

    elif cmd == "info":
        return await s(
            TextCommandsUtil.data_template.format(
                message, bool(message.guild.mfa_level == 1)
            )
        )

    elif cmd == "report":
        return await GitHubUtil.report(s, g, args, message)

    elif cmd == "iss":
        m = await s("Calculating...")
        imp = ISSimp()
        lat = imp.lat()
        lon = imp.lon()
        geodata = search((lat, lon))
        location = "{0}, {1}".format(geodata[0]["admin1"], geodata[0]["cc"])

        await m.delete()
        return await s(
            embed=EmbedUtil.prep(
                "International Space Station", "Where it is right now!"
            )
            .add_field(
                name="Location above Earth", value=str(location), inline=False
            )
            .add_field(name="Latitude", value=str(lat), inline=False)
            .add_field(name="Longitude", value=str(lon), inline=False)
        )

    elif cmd == "fact":
        return await s(embed=EmbedUtil.prep("Random Fact", FactImp().fact()))

    elif cmd == "slots":
        slotz = result()
        top = row()
        btm = row()
        form = "lose"
        if slotz[0] != 0:
            form = "win"
        return await s(
            f"⠀{top[0]}{top[1]}{top[2]}\n"
            # the line above contains unicode, DO NOT REMOVE
            + f"**>** {slotz[1][0]}{slotz[1][1]}{slotz[1][2]} **<**\n"
            + f"   {btm[0]}{btm[1]}{btm[2]}"
            + f"\n**You {form}!**"
        )

    elif cmd == "reboot":
        if str(message.author) in UserUtil.contributors():
            await s("Restarting. This may take up to 5 minutes.")
            # make the bot crash, forcing our server to turn it back on
            _exit(1)
        else:
            return await s(":x: **You are not authorized to run this!**")

    elif cmd == "stars":
        try:
            return await s(
                f"`{args[0]}` has *{g.get_repo(args[0]).stargazers_count}* stars."
            )
        except:
            return await s(
                "Failed to get count. Is the repository valid and public?"
            )

    elif cmd == "homepage":
        try:
            url_nullable = g.get_repo(args[0]).homepage
            if url_nullable is None:
                url_nullable = "(error: homepage not specified by owner)"
            return await s(
                f"{args[0]}'s homepage is located at {url_nullable}"
            )
        except:
            return await s(
                "Failed to fetch homepage. Is the repository valid and public?"
            )

    elif cmd == "boomer":
        return await s(file=discord.File("content/boomer.jpeg"))

    elif cmd == "cookie" or cmd == "cookies":
        subcommand = args[0]
        args = args[1:]
        userId = TextCommandsUtil.get_mentioned_id(args)

        if subcommand == "balance" or subcommand == "bal":
            user = Database.get_user_by_id(userId)

            if userId is None:
                # assume user wants themself
                user = Database.get_user_by_id(message.author.id)

            return await s(
                embed=EmbedUtil.prep(
                    title="Cookies",
                    description=f"User has {user.cookie_count} cookies.",
                )
            )

        elif subcommand == "give" or subcommand == "to":
            user = Database.get_user_by_id(userId)

            if Preconditions.canGetCookie(user):
                user.cookie_count += 1
                user.last_got_cookie_at = datetime.now()
                Database.commit()
                return await s(
                    f"Gave <@!{userId}> a cookie. They now have {user.cookie_count} cookies."
                )

            return await s(
                ":x: *This user has already recieved a cookie in the last hour!*"
            )

        elif subcommand == "admin:set":
            if str(message.author) in UserUtil.admins():
                Database.get_user_by_id(int(args[0])).cookie_count = args[1]
                return await s("Done.")
            else:
                return await s(":x: **You are not authorized to run this!**")

    elif cmd == "admin:reset":
        if str(message.author) in UserUtil.admins():
            Database.session.delete(
                Database.get_user_by_id(
                    TextCommandsUtil.get_mentioned_id(args)
                )
            )
            return await s("Done.")
        else:
            return await s(":x: **You are not authorized to run this!**")

    elif cmd == "define":
        if wordsapi_token is None:
            return await s("This command is disabled due to a configuration error on my host's end - didn't find a WordsAPI token in the config!")
        return await s(embed=TextCommandsUtil.define(args, wordsapi_token))


BotUtil.wrap(client, update_servers)

if __name__ == "__main__":
    logger.info(f"Using discord.py version {discord.__version__}")
    client.run(config["tokens"]["discord"])  # type: ignore
