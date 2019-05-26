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
import random
from discord.utils import get
import FileUtil
import ConfigUtil
import ServerUtil

Bot_Prefix = "+"
client = discord.Client()
log_file = FileUtil.FileHandler(FileUtil.AbstractFile("/home/jumbocakeyumyum/cakebot/rocks.rdil.cakebot.log"))
servers = ConfigUtil.get_servers()


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="BETA! Run +help", type=1))
    print(area4.divider(1))
    print("Ready to roll, I'll see you on Discord: @" + client.user.__str__())
    print(area4.divider(1))


# Called on message event
@client.event
async def on_message(message):
    # Check if this message was authored by the bot:
    if message.author == client.user:
        return

    # Check if message starts with the prefix:
    if not message.content.startswith(Bot_Prefix):
        # log it
        log_file.get_file().wrap().write(
            "[Message Log] Sent by "
            + str(message.author)
            + " on server "
            + message.server.name
            + ": "
            + message.content
        )
        # cancel now
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
        await client.send_message(
            message.channel,
            embed=EmbedUtil.build_help_menu(EmbedUtil.prep(
                title="Cakebot Help",
                description="Make sure to add a + before each command!"
            ))
        )

    elif cmd == "ping":
        await client.send_message(message.channel, "🏓")

    elif cmd == "invite":
        await client.send_message(message.channel, embed=EmbedUtil.prep("Invite CakeBot", "[Click here to invite me!](https://discordapp.com/oauth2/authorize?client_id=580573141898887199&scope=bot&permissions=8)"))

    #elif cmd == "beta":
    #    print (servers[str(message.server.id)]["beta_features"])
    #    # toggle beta command
    #    state = servers[str(message.server.id)]["beta_features"]
    #    if False:
    #        # has perms to toggle
    #        # switch it to the state it isn't (toggle it)
    #        ConfigUtil.toggle_state(str(message.server.id), "beta_features", not state)
    #    else:
    #        # doesnt have perms
    #        await client.send_message(message.channel, "**Sorry, but you do not have the manage server permission, have somebody with it use this command instead!**")

    elif cmd == "8":
        ball = open("/home/jumbocakeyumyum/cakebot/content/8ball.txt", mode="r")
        ball = ball.readlines()
        opt = ball[random.randint(0, int(len(ball) - 1))]
        await client.send_message(
            message.channel,
            embed=EmbedUtil.prep("**" + opt + "**", area4.divider(7) + area4.divider(7))
        )
        

# make the welcome embed
def build_welcome_embed(base):
    base.add_field(
        name="Heya!!",
        value="Today is a great day, "
              + "because today I get the honor of joining this server :D",
        inline=False
    )
    return base


# When the bot joins a server:
@client.event
async def on_server_join(server):
    # add the server ID
    servers = ConfigUtil.add_server(str(server.id), ConfigUtil.get_servers())
    # Send welcome embed
    await client.send_message(ServerUtil.get_general(server),
        embed=build_welcome_embed(
            base=EmbedUtil.prep(
                title="Server Welcome!",
                description=":::::::::::::::::"
            )
        )
    )


# check if user has a role:
def hasRole(server, role_name, person):
    item = get(server.roles, name=role_name)
    if item in person.roles:
        return True
    return False


# read the token:
with open("/home/jumbocakeyumyum/cakebot/token.txt", mode="r") as fh:
    # run the client with the fetched token (stripped of newlines):
    client.run(fh.readlines()[0].replace("\n", ""))
