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

from os import listdir
from discord import AutoShardedClient


class ExtensionLoader:
    extensions: list

    def __init__(self):
        self.extensions = []

    def find_extensions(self) -> list:
        files = listdir("extensions")
        exts = []

        for extension in files:
            if extension.endswith(".py"):
                exts.append(extension)

        return exts

    def bootstrap(self, bot: AutoShardedClient):
        try:
            for e in self.find_extensions():
                inst = __import__("extensions." + e)
                inst.init(bot)
                print("Loaded extension " + e)
                self.extensions.append(e)
        except Exception as exc:
            print("Extension loading error: " + exc.__str__())

    async def on_message(self, message):
        for e in self.extensions:
            await e.on_message(message)

    async def on_command(self, command, args, message):
        for e in self.extensions:
            await e.on_command(command, args, message)

    async def on_message_delete(self, message):
        for e in self.extensions:
            await e.on_message_delete(message)
