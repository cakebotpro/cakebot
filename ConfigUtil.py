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

import json
import FileUtil

default_options = {
    'beta_features': False
}


# add to the server config when a bot joins a new server
def add_server(server_id, server_list):
    # Checks for duplicates
    for s_id in server_list.keys():
        if s_id == server_id:
            return

    server_list[server_id] = default_options

    # Write to file
    with FileUtil.AbstractFile("/home/jumbocakeyumyum/cakebot/serveropts.json").wrap() as config:
        config.write(json.dumps({"servers": server_list}, indent=1))
        config.close()


# reads in the config
def get_servers():
    with open("/home/jumbocakeyumyum/cakebot/serveropts.json", "r") as config:
        servers = json.load(config)
        return servers["servers"]
