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
import random
import github
import reverse_geocoder as rg
from club.cakebot import FileUtil, EmbedUtil, ServerUtil, TextCommandsUtil, Bootstrap
from club.cakebot.external.NASAData import ApiImp
from club.cakebot.external.FactData import ApiImpTwo
from lcbools import true, false

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(filename='/home/jumbocakeyumyum/cakebot/discord.log', encoding='utf-8', mode='w'))

# github endpoint
github.enable_console_debug_logging()
g = github.Github(open("/home/jumbocakeyumyum/cakebot/tokengh.txt", mode="r").readlines()[0].replace("\n", ""))

Bot_Prefix = "+"
client = discord.Client()
# servers = ConfigUtil.get_servers()


# this *needs* to be a runnable object,
# so just ignore it please
def t():
    return true


@client.event
async def on_ready():
    Bootstrap.bootstrap(client, FileUtil.FileHandler(FileUtil.AbstractFile("/home/jumbocakeyumyum/cakebot/servers.txt")))
    await client.change_presence(game=discord.Game(name="Heya! Run +help", type=1))
    print(area4.divider(1))
    print("Ready to roll, I'll see you on Discord: @" + client.user.__str__())
    print(area4.divider(1))


# Called on message event
@client.event
async def on_message(message):
    # Check if message starts with the prefix:
    if not message.content.startswith(Bot_Prefix):
        # cancel
        return

    # Split the input
    theinput = message.content[len(Bot_Prefix):]

    args = theinput.split()

    # the command, e.x. "help"
    cmd = args[0].lower()

    # the args (array) e.x. ["hello", "world"]
    args = args[1:]

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
        await client.send_message(message.channel, embed=EmbedUtil.prep(
            "Invite Cakebot",
            "[Click here to invite me!](https://discordapp.com/oauth2/"
            + "authorize?client_id=580573141898887199&scope=bot&permissions=8)"
        ))

    # TODO: beta toggling

    elif cmd == "8":
        await client.send_message(
            message.channel,
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
        await client.send_message(
            message.channel,
            embed=EmbedUtil.prep(
                "**"
                + TextCommandsUtil.jokes()
                + "**",
                area4.divider(7)
                + area4.divider(7)
            )
        )

    # TODO: perms system

    elif cmd == "info":
        await client.send_message(
            message.channel,
            '***{0}***\n**Owner:** {1}\n**Members:** {2}\n**Region:** {3}\n**Server ID:** {4}'.format(
                message.server.name,
                message.server.owner,
                len(message.server.members),
                message.server.region,
                message.server.id
            )
        )

    elif cmd == "report":
        repo = g.get_repo("RDIL/cakebot")
        String = ""
        for e, z in enumerate(args):
            args[e] = str(args[e]) + " "
        repo.create_issue(title="Support ticket #" + str(random.randint(0, 1000000)), body=str(f"## Support Ticket\n> Filed by {message.author.__str__()}\n### Message:\n`{str(String.join(args))}`\n##### Powered by Cakebot | https://cakebot.club"))
        await client.send_message(message.channel, ":white_check_mark: **Our team has been notified.**")

    elif cmd == "iss":
        m = await client.send_message(message.channel, "Calculating...")
        imp = ApiImp()
        lat = imp.isslat()
        lon = imp.isslon()
        geodata = rg.search((lat, lon))
        location = "{}, {}".format(geodata[0]["admin1"], geodata[0]["cc"])

        embed = EmbedUtil.prep("International Space Station", "Where it is at right now!")
        embed.add_field(name="Location above Earth", value=str(location), inline=false)
        embed.add_field(name="Latitude", value=str(lat), inline=false)
        embed.add_field(name="Longitude", value=str(lon), inline=false)
        await client.send_message(message.channel, embed=embed)
        await client.delete_message(m)

    elif cmd == "fact":
        await client.send_message(message.channel, embed=EmbedUtil.prep("Random Fact", ApiImpTwo().fact()))

    elif cmd == "cookie":
        if "give" in args:
            for member in message.server.members:
                if "<@{0}>".format(member.id) in args:
                    await client.send_message(message.channel, ":up: You gave " + member.id.__str__() + " a cookie!"))
                    with open("/home/jumbocakeyumyum/cakebot/content/Cookiefile", mode="r") as cf:
                        lines = cf.readlines()
                        # requested
                        for line in lines:
                            if member.id in line:
                                # in file
                                c = int(line.split(" - ")[1])
                                cf.write(f"{member.id} - {c + 1}")
                            else:
                                cf.write(f"{member.id} - 1")  # first cookie :D
        elif "count" in args:
            # get count
            with open("/home/jumbocakeyumyum/cakebot/content/Cookiefile", mode="r") as cf:
                lines = cf.readlines()
                for member in message.server.members:
                    if "<@{0}>".format(member.id) in args:
                        # requested
                        for line in lines:
                            if member.id in line:
                                # in file
                                st = " - "
                                await client.send_message(message.channel, f"person has {line.split(st)[1]} cookies"))
                            else:
                                await client.send_message(message.channel, "person has no cookies"))
        else:
            if len(args) == 0:
                await client.send_message(message.channel, "I'm confused!" +
                                          "[See the docs please](https://cakebot.club/commands.html)."
                                         )
            else:
                await client.send_message(message.channel, "Hmm... I don't understand what '" + "' means." +
                                          "[See the docs please](https://cakebot.club/commands.html)."
                                         )


# make the welcome embed
def build_welcome_embed(base):
    base.add_field(
        name="Heya!!",
        value="Today is a great day, "
              + "because today I get the honor of joining this server :D",
        inline=false
    )
    return base


# When the bot joins a server:
@client.event
async def on_server_join(server):
    # Send welcome embed
    await client.send_message(
        ServerUtil.get_general(server),
        embed=build_welcome_embed(
            base=EmbedUtil.prep(
                title="Server Welcome!",
                description="================"
            )
        )
    )


# read the token:
with open("/home/jumbocakeyumyum/cakebot/token.txt", mode="r") as fh:
    # run the client with the fetched token (stripped of newlines):
    client.run(fh.readlines()[0].replace("\n", ""))
