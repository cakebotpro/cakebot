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
import EmbedUtil
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
    print("Ready to roll, I'll see you on Discord: @", client.user)
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
    TODO: theinput = message.content[len(Bot_Prefix):]
    args = theinput.split()
    # the command, e.x. "help"
    cmd = args[0].lower()
    if cmd is None:
        # fix npe
        return
    if cmd is "" or cmd is " ":
        # fix npe
        return
    # the args (array) e.x. ["hello", "world"]
    # TODO: args = args[1:]


@client.event
async def on_server_join(server):
    await client.send_message(
        get_general(),
        embed=EmbedUtil.classic(
            name="Server Welcome!",
            description=":::::::::::::::::",
            sectionNames=[
                "Hello!"
            ],
            sectionContents=[
                "Today is a great day, because today I have been invited"
                +"to this server! I hope to have fun here!"
            ]
        )
    )


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
    return False


def get_general(server):
    """
    Get the general chat room for the server

    :return: the channel if found
    :param server: the server object to check
    """
    check_for = [
        get(server.channels, name='general')
        get(server.channels, name='hub')
        get(server.channels, name='chat')
        get(server.channels, name='talk')
        get(server.channels, name='info')
        get(server.channels, name='announcements')
        get(server.channels, name='welcome')
        get(server.channels, name='commands')
    ]

    for e, v in enumerate(check_for):
        if check_for[e] in server.channels:
            return check_for[e]
    return


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    client.run(token)
else:
    raise Exception("Bot can't be imported!")
