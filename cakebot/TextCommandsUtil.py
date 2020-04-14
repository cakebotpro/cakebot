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
from typing import Any, Dict, List, Union

from discord import Message
from requests import get

from cakebot import EmbedUtil


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


def define(args: List[str], token: str) -> EmbedUtil.Embed:
    """Defines a word."""

    word = args[0]
    headers = {
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "x-rapidapi-key": token,
    }
    definition = get(
        "https://wordsapiv1.p.rapidapi.com/words/" + word, headers=headers
    )
    resp = definition.json()

    e = EmbedUtil.prep(
        title=word.capitalize(), description="Data for this word:"
    )
    try:
        e.add_field(
            name="Syllables",
            value=", ".join(resp["syllables"]["list"]),
            inline=True,
        )
    except KeyError:
        e.add_field(
            name="Error", value="I don't think I know this word!", inline=True
        )

    e = parse_define_json(e, resp)
    return e


def parse_define_json(
    embed: EmbedUtil.Embed, json: Dict[str, Any]
) -> EmbedUtil.Embed:
    """Parses the `results` of the `define` JSON."""

    definitions = json["results"]
    e: EmbedUtil.Embed = embed

    for index, obj in enumerate(definitions[:8]):  # up to first 8 definitions
        e.add_field(
            "Definition " + str(index + 1), obj["definition"], inline=False
        )

    return e


data_template = """\
***{0}***
**Owner:** {1}
**Members:** {2}
**Region:** {3}
**Server ID:** {4}
**Nitro Booster Count:** {5}
**Icon Is Animated:** {6}
**Created At:** {7}
**More Than 250 Members:** {8}
**Admins Need 2-Factor Auth: {9}
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

    elif cmd == "say":
        return " ".join(args)

    elif cmd == "joke":
        return common("jokes")

    return None
