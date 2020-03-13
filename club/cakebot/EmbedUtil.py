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

from discord import Embed
from . import ColourUtil


def prep(title, description):
    embed = Embed(
        title=title, description=description, color=ColourUtil.random()
    )
    embed.set_footer(
        text="Created with ❤ and 🍪 by the Cakebot Team | https://cakebot.club/"
    )
    embed.set_author(
        name="Cakebot",
        url="https://cakebot.club",
        icon_url="https://raw.githubusercontent.com/cakebotpro/cakebot/master/content/cake.png",
    )
    return embed
