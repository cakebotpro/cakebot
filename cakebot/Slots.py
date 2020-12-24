"""
Cakebot - A fun and helpful Discord bot
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

from random import choice, randint

emojis = "🍎🍊🍐🍋🍉🍇🍒"  #: The emojis that the game picks from.


def row():
    # type: () -> list
    """
    Returns a row of 3 emojis (as an array).

    Example: ["🍊", "🍉", "🍇"]
    """

    return [choice(emojis), choice(emojis), choice(emojis)]


def result():
    # type: () -> list
    """
    Returns the result of the game.

    This will be an array, consisting of the following data:
    - A number (either 0 or 1), 0 means you lose and 1 means you win
    - The row of emojis selected (see the row function documentation)
    """

    r = row()

    if r[0] == r[1] == r[2]:
        return [1, r]

    if randint(0, 5) == 4:
        # give player actual chance
        ic = str(choice(emojis))
        return [1, [ic, ic, ic]]

    return [0, r]
