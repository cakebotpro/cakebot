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

from os import getenv
from sys import exit as _exit

import discord
import yappi
from click import group, option, secho, version_option
from discord.utils import oauth_url
from factdata import FactImp
from filehandlers import AbstractFile, FileManipulator
from github import Github
from slots import result, row

from cakebot import (
    Database,
    EmbedUtil,
    GitHubUtil,
    IssApi,
    Preconditions,
    TextCommandsUtil,
    UserUtil,
)

config = FileManipulator(AbstractFile("config.json"))
base_conf = {}

if getenv("TEST_ENV") != "yes":
    try:
        base_conf = config.load_from_json()
    except:
        TextCommandsUtil.noop()


g = Github(base_conf.get("tokens", {}).get("github"))
wordsapi_token = base_conf.get("tokens", {}).get("wordsapi", None)
has_enabled_sentry = getenv("PRODUCTION") is not None
client = discord.AutoShardedClient()


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(name=base_conf["status"])
    )
    secho(
        "\nReady to roll, I'll see you on Discord: @" + str(client.user),
        fg="green",
    )


@client.event
async def on_message(message):
    Bot_Prefix = "+"
    if getenv("PRODUCTION") is None:
        Bot_Prefix = "-"

    if not message.content.startswith(Bot_Prefix):
        return

    if has_enabled_sentry:
        from sentry_sdk import configure_scope

        with configure_scope() as scope:
            # show username of discord user in sentry
            scope.user = {
                "id": message.author.id,
                "username": str(message.author),
            }

    # Split input
    args = message.content[len(Bot_Prefix) :].split()

    if len(args) == 0:
        return

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
        or cmd == "say"
    ) and Preconditions.args_are_valid(args):
        return await s(
            embed=EmbedUtil.prep(
                "That command expected an argument (or arguments), but you didn't give it any!",
                "[Read the docs?](https://cakebot.club/docs/commands/)",
            )
        )

    tcu_result = TextCommandsUtil.handle_common_commands(args, cmd)
    if tcu_result != "":
        return await s(tcu_result)

    if cmd == "help":
        return await s(
            embed=EmbedUtil.prep(
                title="Help",
                description="You can check out [this page of our website](https://cakebot.club/docs/commands/) for a full command list!",
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

    elif cmd == "info":
        return await s(
            TextCommandsUtil.data_template.format(
                message.guild.name,
                str(message.guild.owner),
                len(message.guild.members),
                message.guild.region,
                message.guild.id,
                message.guild.premium_subscription_count,
                str(message.guild.is_icon_animated()),
                str(message.guild.created_at),
                str(message.guild.large),
                str(message.guild.mfa_level == 1),
            )
        )

    elif cmd == "report":
        return await GitHubUtil.report(s, g, args, message)

    elif cmd == "iss":
        m = await s("Calculating...")
        imp = IssApi.IssLocater()
        lat = imp.lat
        lon = imp.lon
        from reverse_geocoder import search

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
        form = "win" if slotz[0] == 1 else "lose"
        return await s(
            f"⠀{top[0]}{top[1]}{top[2]}\n"
            # the line above contains unicode, DO NOT REMOVE
            + f"**>** {slotz[1][0]}{slotz[1][1]}{slotz[1][2]} **<**\n"
            + f"   {btm[0]}{btm[1]}{btm[2]}"
            + f"\n**You {form}!**"
        )

    elif cmd == "reboot":
        if message.author.id in UserUtil.admins():
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
            url = g.get_repo(args[0]).homepage
            if url is None:
                url = "(error: homepage not specified by owner)"
            return await s(f"{args[0]}'s homepage is located at {url}")
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

        if subcommand in ["balance", "bal"]:
            if userId == 0:
                # assume user wants themself
                user = Database.get_user_by_id(message.author.id)
            else:
                user = Database.get_user_by_id(userId)

            return await s(
                embed=EmbedUtil.prep(
                    title="Cookies",
                    description=f"User has {user.cookie_count} cookies.",
                )
            )

        elif subcommand in ["give", "to"]:
            if userId == 0:
                return await s(
                    "I don't see who I should give the cookie to. Try mentioning them."
                )
            user = Database.get_user_by_id(userId)

            user.cookie_count += 1
            Database.commit()
            return await s(
                f"Gave <@!{userId}> a cookie. They now have {user.cookie_count} cookies."
            )

        elif subcommand == "admin:set":
            if message.author.id in UserUtil.admins():
                Database.get_user_by_id(userId).cookie_count = args[1]
                return await s("Done.")
            else:
                return await s(":x: **You are not authorized to run this!**")

    elif cmd == "admin:reset":
        if message.author.id in UserUtil.admins():
            Database.session.delete(
                Database.get_user_by_id(
                    TextCommandsUtil.get_mentioned_id(args)
                )
            )
            Database.commit()
            return await s("Done.")
        else:
            return await s(":x: **You are not authorized to run this!**")

    elif cmd == "define":
        if wordsapi_token is None:
            return await s(
                "This command is disabled due to a configuration error on my host's end - didn't find a WordsAPI token in the config!"
            )
        return await s(embed=TextCommandsUtil.define(args, wordsapi_token))

    elif cmd == "start-profiler":
        if message.author.id in UserUtil.admins():
            await s(
                "Started the profiler. Once you are done, run stop-profiler."
            )
            yappi.set_clock_type("wall")
            yappi.start()
        else:
            return await s(":x: **You are not authorized to run this!**")

    elif cmd == "stop-profiler":
        if message.author.id in UserUtil.admins():
            await s("Saved profiler results to `profile.txt`.")
            yappi.stop()
            yappi.get_func_stats().print_all(open("profile.txt", "w"))
        else:
            return await s(":x: **You are not authorized to run this!**")


@group()
@version_option(version="2020.05.08", prog_name="Cakebot")
def cli():
    """The Cakebot command-line-interface."""
    pass


@cli.command()
@option(
    "--discord-token",
    type=str,
    help="Discord token for the bot to use, defaults to the one from the config.json",
    default="",
)
def run(discord_token):
    """Runs the bot."""

    secho("\nStarting Cakebot...\n", fg="blue", bold=True)

    secho("Using discord.py v" + discord.__version__, color="gray")

    if g is None:
        secho(
            "GitHub credentials not found, disabling functionality.",
            fg="white",
        )
    if wordsapi_token is None:
        secho(
            "WordsAPI credentials not found, disabling functionality.",
            fg="white",
        )

    if has_enabled_sentry:
        from discord_sentry_reporting import use_sentry

        use_sentry(
            client,
            dsn="https://e735b10eff2046538ee5a4430c5d2aca@sentry.io/1881155",
            debug=True,
        )

    if discord_token != "":
        client.run(discord_token)
    else:
        client.run(base_conf["tokens"]["discord"])


@cli.command()
def shell():
    """Starts the development shell."""

    from ptpython.repl import embed

    embed(globals(), locals())


if __name__ == "__main__":
    cli()
