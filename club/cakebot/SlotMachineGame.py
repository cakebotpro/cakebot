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

emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"


def get_emojis():
    return emojis


def arraything():
    return [
        random.choice(get_emojis()),
        random.choice(get_emojis()),
        random.choice(get_emojis())
    ]


def result():
    """
    Return codes:
    0 = None in a row     (loss)
    1 = Two in a row      (win)
    2 = All matching      (win)
    :return: whichever int is picked
    :rtype: int
    """
    results = arraything()

    if (
        results[0] == results[1] == results[2]
    ):
        return [2, results]
    elif (
        (results[0] == results[1]) or
        (results[0] == results[2]) or
        (results[1] == results[2])
    ):
        return [1, results]
    else:
        return [0, results]
