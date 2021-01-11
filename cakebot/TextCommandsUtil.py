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

make_server_info = """\
***{0}***
:crown: **Owner:** {1}
:grinning: **Members:** {2}
:map: **Region:** {3}
:id: **Server ID:** {4}
:comet: **Nitro Booster Count:** {5}
:archery: **Icon Is Animated:** {6}
:timer: **Created At:** {7}
:chart_with_upwards_trend: **More Than 250 Members:** {8}
:lock: **Admins Need 2-Factor Auth**: {9}
:purple_circle: **Nitro Server Tier**: {10}
""".format


def handle_common_commands(args, cmd, message):
    # type: (list, str, Message) -> CommonCommandResultHolder
    """Handles certain simple commands."""

    elif cmd == "icon":
        return with_message(str(message.guild.icon_url))
