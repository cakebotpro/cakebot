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
import logging
import filehandlers as fhm
import github
import sys
import area4
import cookies
from fbootstrap import bootstrap
from reverse_geocoder import search
from discord.utils import oauth_url
from slots import row, result
from iss import Imp as ISSimp
from factdata import FactImp
from random import randint
from requests import get
from bs4 import BeautifulSoup as HTML
from lcpy import false
from club.cakebot import TextCommandsUtil, EmbedUtil, UserUtil


logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w'))
logger.addHandler(logging.StreamHandler(sys.stdout))


j = open("tokens.txt", mode="r").readlines()
for i, l in enumerate(j):
    j[i] = j[i].replace("\n", "")


servers = fhm.FileHandler(fhm.AbstractFile("servers.txt"))

github.enable_console_debug_logging()
g = github.Github(j[1])

client = discord.AutoShardedClient()


def update_servers():
    bootstrap(client, servers)
    servers.refresh()


@client.event
async def on_ready():
    fbootstrap.bootstrap(client, servers)
    await client.change_presence(activity=discord.Game(name="Heya! Run +help"))
    logger.info("Ready to roll, I'll see you on Discord: @" + client.user.__str__())


@client.event
async def on_shard_ready(shard_id):
    logger.info(f"Shard {shard_id} is now ready.")


@client.event
async def on_message(message):
    Bot_Prefix = "+"
    if not message.content.startswith(Bot_Prefix):
        return

    # Split input
    args = message.content[len(Bot_Prefix):].split()

    cmd = args[0].lower()

    # the arg array ex. ["hello", "world"]
    args = args[1:]

    # channel
    s = message.channel.send

    if cmd == "help":
        await s(embed=EmbedUtil.help_menu())

    elif cmd == "ping":
        await s("🏓")

    elif cmd == "invite":
        await s(
            embed=EmbedUtil.prep(
                "Invite Cakebot",
                f"[Click here to invite me!]({oauth_url(580573141898887199, permissions=discord.Permissions.all())})"
            )
        )

    elif cmd == "8":
        await s(
            embed=EmbedUtil.prep(
                "**"
                + TextCommandsUtil.eightball()
                + "**",
                area4.divider(7)
                + area4.divider(7)
                + area4.divider(7)
            )
        )

    elif cmd == "joke":
        await s(embed=EmbedUtil.prep(f'**{TextCommandsUtil.jokes()}**', f'{area4.divider(7)}{area4.divider(7)}'))

    elif cmd == "info":
        await s(
            f'***{message.guild.name}***\n**Owner:** {message.guild.owner}\n**Members:** {len(message.guild.members)}\n**Region:** {message.guild.region}\n**Server ID:** {message.guild.id}'
        )

    elif cmd == "report":
        repo = g.get_repo("cakebotpro/cakebot")
        String = ""
        for e, z in enumerate(args):
            args[e] = str(args[e]) + " "
        repo.create_issue(
            title="Support ticket #" + str(randint(0, 100000)),
            body=str(f"## Support Ticket\n> Filed by {message.author.__str__()}\n### Message:\n`{str(String.join(args))}`\n##### Powered by Cakebot | https://cakebot.club"),
            labels=[repo.get_label("ticket")]
        )
        await s(":white_check_mark: **Our team has been notified.**")

    elif cmd == "iss":
        m = await s("Calculating...")
        imp = ISSimp()
        lat = imp.lat()
        lon = imp.lon()
        geodata = search((lat, lon))
        location = "{0}, {1}".format(geodata[0]["admin1"], geodata[0]["cc"])

        await m.delete()
        await s(
            embed=EmbedUtil.prep(
                "International Space Station", "Where it is right now!"
            ).add_field(
                name="Location above Earth", value=str(location), inline=false
            ).add_field(
                name="Latitude", value=str(lat), inline=false
            ).add_field(
                name="Longitude", value=str(lon), inline=false
            )
        )

    elif cmd == "fact":
        await s(embed=EmbedUtil.prep("Random Fact", FactImp().fact()))

    elif cmd == "slots":
        slotz = result()
        top = row()
        btm = row()
        form = "lose"
        if slotz[0] != 0:
            form = "win"
        await s(
            ""
            + f"⠀{top[0]}{top[1]}{top[2]}\n"
            # the line above contains unicode, DO NOT REMOVE
            + f"**>** {slotz[1][0]}{slotz[1][1]}{slotz[1][2]} **<**\n"
            + f"   {btm[0]}{btm[1]}{btm[2]}"
            + f"\n**You {form}!**"
        )

    elif cmd == "define":
        c = ""
        if len(args) < 1:
            await s(":x: *You need to specify a word!*")
            return
        if len(args) > 1:
            for i, h in enumerate(args):
                c = str(c + args[i] + "%20")
        else:
            c = args[0]
        sm = HTML(get(f"https://www.merriam-webster.com/dictionary/{c}").content, "html.parser").find(
            "span", attrs={"class": "dtText"}
        ).text
        await s(f"{c}{sm}")

    elif cmd == "cookie":
        cookie_class = cookies.Cookie("Cookiefile")
        if args[0] == "give":
            try:
                logger.warn(f"trying to give cookie to {args[1]}")
                cookie_class.give(args[1])
            except IndexError:
                await s(":x: **Failed to run command.**")
        elif args[0] == "balance":
            try:
                user = args[1]
            except IndexError:
                user = str(message.author)
            await s(f"{str(message.author)} has {cookie_class.get_balance(user)} cookies.")

    elif cmd == "restart":
        if str(message.author) in UserUtil.get_contributors():
            await s("Restarting. *This may take up to 5 minutes*.")
            # make the bot crash, forcing our server to turn it back on
            sys.exit(1)
        else:
            await s("**You are not authorized to run this!**")


@client.event
async def on_guild_join(guild):
    update_servers()
    await guild.channels[0].send(embed=EmbedUtil.prep(title="Heya!", description="Today is a great day, because I get the honor of joining this server :D"))


@client.event
async def on_guild_remove(guild):
    update_servers()


@client.event
async def on_guild_update(guild):
    update_servers()


client.run(j[0])
