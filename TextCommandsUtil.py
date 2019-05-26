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

import random


def eightball():
    var1 = common_reader("8ball.txt")
    return var1[random.randint(0, int(len(var1) - 1))]


def jokes():
    var1 = common_reader("jokes.txt")
    return var1[random.randint(0, int(len(var1) - 1))]


def common_reader(filename):
    var1 = open("/home/jumbocakeyumyum/cakebot/content/" + filename, mode="r")
    return var1.readlines()
