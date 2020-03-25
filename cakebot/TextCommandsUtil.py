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

from random import choice
from requests import get
from cakebot import EmbedUtil
from typing import List, Union
from discord import Message


def common(name: str) -> str:
    """Load a content file and pick a random line from it (used a lot)."""

    fileobj = open("content/" + name + ".txt", mode="r")
    lines = fileobj.readlines()
    fileobj.close()
    return choice(lines)


def noop():
    """Literally just do nothing (for the purpose of avoiding syntax errors)."""
    return


def get_mentioned_id(args: List[str]) -> Union[int, None]:
    """Checks a list of arguments for a valid Discord mention."""
    for arg in args:
        base = arg
        if arg.startswith("<@!") and arg.endswith(">"):
            # strip out the divider chars
            base = base.replace("<@!", "")
            base = base.replace(">", "")
        try:
            if int(base) > 100000:
                return int(base)
        except ValueError:
            noop()
    return None


def define(args: List[str], token: str):
    """Defines a word."""

    word = args[0]
    headers = {
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "x-rapidapi-key": token,
    }
    definition = get(
        "https://wordsapiv1.p.rapidapi.com/words/" + word, headers=headers
    )
    return EmbedUtil.prep(title=definition.json(), description="")


data_template = """\
***{0.guild.name}***
**Owner:** {0.guild.owner}
**Members:** {len(0.guild.members)}
**Region:** {0.guild.region}
**Server ID:** {0.guild.id}
**Nitro Booster Count:** {0.guild.premium_subscription_count}
**Icon Is Animated:** {str(0.guild.is_icon_animated())}
**Created At:** {str(0.guild.created_at)}
**More Than 250 Members:** {str(0.guild.large)}
**Admins Need 2-Factor Auth: {1}
"""


def handle_common_commands(
    message: Message, args: List[str], cmd: str
) -> Union[str, None]:
    """Handles certain simple commands."""

    if cmd == "pi":
        return "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709"

    elif cmd == "coinflip":
        return choice(["**Heads**.", "**Tails**."])

    elif cmd == "8":
        return common("8ball")

    elif cmd == "clapify":
        return " :clap: ".join(args)

    return None
