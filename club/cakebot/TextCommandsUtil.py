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

from random import randint


def common(n):
    var1 = open("content/" + n + ".txt", mode="r").readlines()
    return var1[randint(0, int(len(var1) - 1))]


def clapify(args):
    s = ""
    for arg in args:
        if s == "":
            s = str(arg + " ")
        else:
            s += str(":clap: " + arg + " ")
    return s


def get_mentioned_id(message_contents):
    for item in message_contents:
        if item.startswith("<@!") and item.endswith(">"):
            base = item
            # strip out the divider chars
            base = base.replace("<@!", "")
            base = base.replace(">", "")
            return int(base)
    return None
