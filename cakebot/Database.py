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

from typing import Any
from json import dumps


class DiscordUser:
    id: int
    cookie_count: int

    def __repr__(self):
        # type: () -> str
        return "<DiscordUser {0} {1}>".format(self.id, self.cookie_count)

    @staticmethod
    def from_json(id, json):
        # type: (dict) -> DiscordUser
        u = DiscordUser()
        u.id = id
        u.cookie_count = json["cookie_count"]
        return u


def get_user_by_id(id, file_man):
    # type: (int, Any) -> DiscordUser
    """
    Finds a user in the database from their Discord ID,
    and creates an entry if they don't exist yet.
    """

    u = None
    tmp = file_man.load_from_json()
    for user in tmp["users"]:
        if user == id:
            u = user

    if u is None:
        tmp["users"][id] = {"cookie_count": 0}
        file_man.write(dumps(tmp))
        file_man.refresh()

    return DiscordUser.from_json(id, tmp["users"][id])
