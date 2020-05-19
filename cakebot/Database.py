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


class DiscordUser:
    id: int
    cookie_count: int

    def __repr__(self):
        # type: () -> str
        return "<DiscordUser {0} {1}>".format(self.id, self.cookie_count)

    @staticmethod
    def from_json(json):
        # type: (dict) -> DiscordUser
        u = DiscordUser()
        u.id = json["id"]
        u.cookie_count = json["cookie_count"]
        return u

    @staticmethod
    def create(id):
        # type: (int) -> DiscordUser
        return DiscordUser.from_json({"id": id, "cookie_count": 0})


def get_user_by_id(id):
    # type: (int) -> DiscordUser
    """
    Finds a user in the database from their Discord ID,
    and creates an entry if they don't exist yet.
    """

    return DiscordUser()
