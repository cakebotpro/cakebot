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
import os
from discord.utils import get

Bot_Prefix = "+"

client = discord.ext.commands.Bot(command_prefix=Bot_Prefix)


@client.event
async def on_ready():
    """
    Called when the bot is booted

    :return: nothing
    :rtype: None
    """
    await client.change_presence(game=discord.Game(name="Being beta tested"))

    print(area4.divider(1))
    print("Ready to role, I'll see you on Discord: @", client.user)
    print(area4.divider(1))


@client.event
async def on_message(message):
    """
    Called on message

    :return: nothing
    :rtype: None
    :param message: the message object
    """
    if message.author == client.user:
        # cancel own messages
        return
    if not message.content.startswith(Bot_Prefix):
        # normal message
        return
    # asking for bot
    theinput = message.content[len(prefix):]
    args = theinput.split()
    # the command, e.x. "help"
    cmd = args[0].lower()
    # the args (array) e.x. ["hello", "world"]
    args = args[1:]


def hasRole(server, role_name, person):
    """
    If user has a role

    :param server: the discord server object
    :param role_name: the name of the role as a string
    :param person: the person to check
    :return: if they have it or not
    :rtype: bool
    """
    item = get(server.roles, name=role_name)
    if item in person.roles:
        return True
    else:
        return False


if __name__ == __main__:
    token = os.getenv("TOKEN")
    client.run(token)
else:
    raise Exception("Bot can't be imported!")
