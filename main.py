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
import area4
import logging
import filehandlers as fhm
import github
import sys
import fbootstrap
from club.cakebot import OnMessage, ServerUtil


logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(filename='/home/jumbocakeyumyum/cakebot/discord.log', encoding='utf-8', mode='w'))
logger.addHandler(logging.StreamHandler(sys.stdout))


j = open("/home/jumbocakeyumyum/cakebot/tokens.txt", mode="r").readlines()
for i, l in enumerate(j):
    j[i].replace("\n", "")


github.enable_console_debug_logging()
g = github.Github(j[1])


client = discord.AutoShardedClient()


@client.event
async def on_ready():
    fbootstrap.bootstrap(client, fhm.FileHandler(fhm.AbstractFile("/home/jumbocakeyumyum/cakebot/servers.txt")))
    await client.change_presence(activity=discord.Streaming(name="Heya! Run +help", url="https://cakebot.club"))
    logger.info("Ready to roll, I'll see you on Discord: @" + client.user.__str__())


@client.event
async def on_message(message):
    OnMessage.om(client, g, message, logger, j)


@client.event
async def on_guild_join(guild):
    await ServerUtil.get_general(guild).send_message(embed=EmbedUtil.prep(title="Heya!", description="Today is a great day, because I get the honor of joining this server :D"))


client.run(j[0])
