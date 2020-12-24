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

# THIS FILE IS MEANT TO CONTROL ACCESS TO THE BOT.
# YOU MAY EDIT THIS IF YOU ARE SELF-HOSTING IT TO CONTROL ITS BEHAVIOR.


def admins():
    # type: () -> list
    """Returns a list of IDs for people with administrator access."""

    return [411505437003743243, 304005557797257216]


def banned_users():
    # type: () -> list
    """
    Returns a list of IDs for people who CANNOT RUN ANY BOT COMMANDS.
    This is helpful for if you are being spammed with potentially harmful commands, like report.
    """
    return [649431206881918979, 440269487321776133, 791695274296082462]
