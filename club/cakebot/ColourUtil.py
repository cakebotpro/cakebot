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
from colour import Tan
import random


def randomcolor():
    colors = [
        Color.teal(),
        Color.dark_teal(),
        Color.green(),
        Color.dark_green(),
        Color.blue(),
        Color.dark_blue(),
        Color.purple(),
        Color.dark_purple(),
        Color.magenta(),
        Color.dark_magenta(),
        Color.gold(),
        Color.dark_gold(),
        Color.orange(),
        Color.dark_orange(),
        Color.red(),
        Color.dark_red(),
        Color.lighter_grey(),
        Color.darker_grey(),
        Tan.tan()
    ]
    intobj = random.randint(0, len(colors) - 1)
    return colors[intobj]
