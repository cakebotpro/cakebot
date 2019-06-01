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

from discord import Color
import random


def randomcolor():
    c = Color()
    colors = [
        c.teal(),
        c.dark_teal(),
        c.green(),
        c.dark_green(),
        c.blue(),
        c.dark_blue(),
        c.purple(),
        c.dark_purple(),
        c.magenta(),
        c.dark_magenta(),
        c.gold(),
        c.dark_gold(),
        c.orange(),
        c.dark_orange(),
        c.red(),
        c.dark_red(),
        c.lighter_grey(),
        c.darker_grey()
    ]
    intobj = random.randint(len(colors))
    return colors[intobj]
