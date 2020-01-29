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

from datetime import datetime


def checkArgsAreNotNull(params):
    return bool(
        len(params) < 1 and
        params is not [] and
        params is not [""] and
        params is not ["", ""]
    )


def argCountIsAtLeast(params, number):
    return len(params) >= number


def canGetCookie(user):
    diff = user.last_got_cookie_at - datetime.now()
    # difference in seconds split into minutes
    mins = int(diff.total_seconds() / 60)
    if mins < 0:
        # for some odd reason, this number is negative
        # so we need to do this :/
        mins += mins * -2
    # if the user got a cookie in the last hour
    return mins > 60
