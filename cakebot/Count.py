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

# workaround for the global variable issue
counter = [0]


# these functions are temporary for a personal server.
# they need to be officially implemented for all servers some time
def increment():
    counter[0] += 1


def get():
    return counter[0]


def set(i):
    counter[0] = i


async def on_message_deleted(message):
    if message.channel.id == 688701770284924932 and not message.author.bot:
        await message.channel.send(
            "Message deleted. The last number was " + str(get())
        )


async def on_message(message):
    if message.channel.id == 688701770284924932 and not message.author.bot:
        try:
            if message.content.startswith("s"):
                set(int(message.content.replace("s", "")))
                return
            if int(message.content) == get() + 1:
                increment()
                return
            await message.delete()
            return
        except Exception:
            await message.delete()
            return
