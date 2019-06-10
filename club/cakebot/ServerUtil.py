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

from discord.utils import get


# get main chat room
def get_general(guild):
    check_for = [
        get(guild.channels, name='general'),
        get(guild.channels, name='hub'),
        get(guild.channels, name='chat'),
        get(guild.channels, name='talk'),
        get(guild.channels, name='info'),
        get(guild.channels, name='announcements'),
        get(guild.channels, name='welcome'),
        get(guild.channels, name='commands')
    ]

    # if a match is found, return the channel object
    for e, v in enumerate(check_for):
        if check_for[e] in guild.channels:
            return check_for[e]
