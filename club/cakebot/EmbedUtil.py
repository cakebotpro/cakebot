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
from club.cakebot import HexBuilder


def prep(title, description):
    # embed metadata
    embed = discord.Embed(
        title=title,
        description=description,
        color=int(HexBuilder.r())
    )
    # footer
    embed.set_footer(text="Created with ❤ and 🍪 by the Cakebot Team | https://cakebot.club/")
    return embed


def build_help_menu(base):
    with open("/home/jumbocakeyumyum/cakebot/content/help.cfg", "r") as optz:
        for line in optz.readlines():
            # strip newlines and parse
            itemm = line.replace("\n", "").split(" -> ")
            base.add_field(name=itemm[0], value=itemm[1], inline=False)
    return base
