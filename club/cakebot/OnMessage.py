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

import area4
import random
import github
import requests
import iss
import factdata
import slots
import reverse_geocoder as rg
from club.cakebot import EmbedUtil, TextCommandsUtil
from lcbools import false

def om(client, github, message, logger, j)
    Bot_Prefix = "+"
    if not message.content.startswith(Bot_Prefix):
        return

    # Split the input
    args = message.content[len(Bot_Prefix):].split()

    cmd = args[0].lower()

    # the arg (array) ex. ["hello", "world"]
    args = args[1:]

    # channel
    s = message.channel.send

    if cmd == "help":
        await s(embed=EmbedUtil.help_menu())

    elif cmd == "ping":
        await s("🏓")

    elif cmd == "invite":
        await s(embed=EmbedUtil.prep("Invite Cakebot",
            "[Click here to invite me!](https://discordapp.com/oauth2/authorize?client_id=580573141898887199&scope=bot&permissions=8)"
        ))

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
            title="Support ticket #" + str(random.randint(0, 100000)),
            body=str(f"## Support Ticket\n> Filed by {message.author.__str__()}\n### Message:\n`{str(String.join(args))}`\n##### Powered by Cakebot | https://cakebot.club")
        )
        await s(":white_check_mark: **Our team has been notified.**")

    elif cmd == "iss":
        m = await s("Calculating...")
        imp = iss.Imp()
        lat = imp.lat()
        lon = imp.lon()
        geodata = rg.search((lat, lon))
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
        await s(embed=EmbedUtil.prep("Random Fact", factdata.FactImp().fact()))

    elif cmd == "slots":
        slotz = slots.result()
        top = slots.row()
        btm = slots.row()
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
        sm = HTML(requests.get(f"https://www.merriam-webster.com/dictionary/{c}").content, "html.parser").find(
            "span", attrs={"class": "dtText"}
        ).text
        await s(f"{c}{sm}")
