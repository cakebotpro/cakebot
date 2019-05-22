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
import EmbedUtil
import area4
from discord.utils import get

Bot_Prefix = "+"

client = discord.Client()


@client.event
async def on_ready():
    print("Changing playing status...")
    await client.change_presence(game=discord.Game(name="Being beta tested"))

    print(area4.divider(1))
    print("Ready to roll, I'll see you on Discord: @" + client.user.name)
    print(area4.divider(1))


# Called on message event
@client.event
async def on_message(message):
    # Check if this message was authored by the bot:
    if message.author == client.user:
        return

    # Check if message starts with the prefix:
    if not message.content.startswith(Bot_Prefix):
        # normal message
        return
    
    # Split the input
    theinput = message.content[len(Bot_Prefix):]
    
    args = theinput.split()
    
    # the command, e.x. "help"
    cmd = args[0].lower()
    
    # if the user doesn't put in a command with the prefix, cancel:
    if cmd is None:
        return
    
    # if the user doesn't put in a command with the prefix, cancel:
    if cmd == "" or cmd == " ":
        # fix npe
        return
    
    # the args (array) e.x. ["hello", "world"]
    args = args[1:]
    
    # make all args lowercase:
    for i in range(len(args)):
        args[i] = args[i].lower()

    # COMMANDS
    if cmd == "help":
        await client.send_message(message.channel,
            embed=EmbedUtil.classic(
                name="Cakebot Help Menu",
                description=":::::::::::::::::",
                sectionNames=[
                    "Basic Commands"
                ],
                sectionContents=[
                    "`help` - Show this menu"
                ]
            )
        )



# When the bot joins a server:
@client.event
async def on_server_join(server):
    # Send welcome embed
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


# check if user has a role:
def hasRole(server, role_name, person):
    item = get(server.roles, name=role_name)
    if item in person.roles:
        return True
    return False


# get main chat room
def get_general(server):
    check_for = [
        get(server.channels, name='general'),
        get(server.channels, name='hub'),
        get(server.channels, name='chat'),
        get(server.channels, name='talk'),
        get(server.channels, name='info'),
        get(server.channels, name='announcements'),
        get(server.channels, name='welcome'),
        get(server.channels, name='commands')
    ]

    # if a match is found, return the channel object
    for e, v in enumerate(check_for):
        if check_for[e] in server.channels:
            return check_for[e]


# read the token:
with open("/home/jumbocakeyumyum/cakebot/token.txt", mode="r") as fh:
    # run the client with the fetched token (stripped of newlines):
    client.run(fh.readlines()[0].replace("\n", ""))
