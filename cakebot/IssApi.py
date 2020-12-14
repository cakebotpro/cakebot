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

from requests import get


class IssLocater:
    """A class that fetches the data from the API to find where the ISS is."""

    def __init__(self):
        """Creates a new instance of the class."""

        obj = get("http://api.open-notify.org/iss-now.json").json()
        self.lat = obj["iss_position"]["latitude"]
        self.lon = obj["iss_position"]["longitude"]
