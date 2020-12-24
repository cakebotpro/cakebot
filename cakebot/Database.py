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

from json import dumps
from typing import Any


def add_cookie(id, file_man):
    # type: (int, Any) -> int
    """
    Gives a users a cookie count and returns the new number.
    """

    u = None
    tmp = file_man.load_from_json()
    for user in tmp["users"]:
        if user == id:
            u = user

    if u is None:
        tmp["users"][id] = {"cookie_count": 1}
        file_man.write_to_file(dumps(tmp))
        file_man.refresh()
        return 1

    tmp["users"][id]["cookie_count"] += 1
    file_man.write_to_file(dumps(tmp, indent=4))
    file_man.refresh()
    return file_man.load_from_json()["users"][id]["cookie_count"]


def get_count(id, file_man):
    # type: (int, Any) -> int

    return file_man.load_from_json()["users"].get(id, {"cookie_count": 0})[
        "cookie_count"
    ]
