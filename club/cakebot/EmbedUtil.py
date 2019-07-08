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
from club.cakebot import ColourUtil


def prep(title, description):
    # embed metadata
    embed = discord.Embed(
        title=title,
        description=description,
        color=ColourUtil.random()
    )
    # footer
    embed.set_footer(text="Created with ❤ and 🍪 by the Cakebot Team | https://cakebot.club/")
    embed.set_author(name="Cakebot", url="https://cakebot.club", icon_url="https://raw.githubusercontent.com/RDIL/cakebot/master/content/cake.png")
    return embed


def help_menu():
    with open("content/help.cfg", "r") as opz:
        k = prep(title="Cakebot Help", description="Make sure to add a + before each command!")
        for line in opz.readlines():
            itm = line.replace("\n", "").split(" -> ")
            k.add_field(name=itm[0], value=itm[1], inline=False)
        return k
