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

import yappi
from random import choice
from requests import get
from cakebot import EmbedUtil, UserUtil
from discord import Message, Embed


def random_from_file(file_name):
    # type: (str) -> str
    """Load a content file and pick a random line from it."""

    fileobj = open("content/" + file_name + ".txt", mode="r")
    lines = fileobj.readlines()
    fileobj.close()
    return choice(lines)


def noop():
    # type: () -> None
    """Literally just do nothing."""
    return


def get_mentioned_id(args):
    # type: (list) -> int
    """Checks a list of arguments for a valid Discord mention."""

    for arg in args:
        base = arg
        if (arg.startswith("<@!") or arg.startswith("<@")) and arg.endswith(
            ">"
        ):
            # strip out the divider chars
            base = base.replace("<@", "")
            base = base.replace("!", "")
            base = base.replace(">", "")
        try:
            if int(base) > 100000:
                return int(base)
        except ValueError:
            noop()
    return 0


def define(args, token):
    # type: (list, str) -> EmbedUtil.Embed
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
            value=", ".join(
                resp.get("syllables", {"list": ["unknown"]})["list"]
            ),
            inline=True,
        )
    except KeyError:
        e.add_field(
            name="Error", value="I don't think I know this word!", inline=True
        )

    e = parse_define_json(e, resp)
    return e


def parse_define_json(embed, json):
    # type: (EmbedUtil.Embed, dict) -> EmbedUtil.Embed
    """Parses the `results` of the `define` JSON."""

    definitions = json["results"]
    e = embed

    for index, obj in enumerate(definitions[:8]):  # up to first 8 definitions
        e.add_field(
            name="Definition " + str(index + 1),
            value=obj["definition"],
            inline=False,
        )

    return e


make_server_info = """\
***{0}***
:crown: **Owner:** {1}
:grinning: **Members:** {2}
:map: **Region:** {3}
:id: **Server ID:** {4}
:comet: **Nitro Booster Count:** {5}
:archery: **Icon Is Animated:** {6}
:timer: **Created At:** {7}
:chart_with_upwards_trend: **More Than 250 Members:** {8}
:lock: **Admins Need 2-Factor Auth**: {9}
""".format


class CommonCommandResultHolder:
    kwargs: dict
    message: str

    def __init__(self, message="", kwargs={}):
        # type: (str, dict) -> None
        self.kwargs = kwargs
        self.message = message


def with_message(message):
    # type: (str) -> CommonCommandResultHolder
    """Helper to return a CommonCommandResultHolder that just sends a message."""
    return CommonCommandResultHolder(message)


def with_embed(embed):
    # type: (Embed) -> CommonCommandResultHolder
    """Helper to return a CommandCommandResultHolder that just sends an embed."""
    return CommonCommandResultHolder(kwargs={embed: embed})


def handle_common_commands(args, cmd, message):
    # type: (list, str, Message) -> CommonCommandResultHolder
    """Handles certain simple commands."""

    if cmd == "pi":
        return with_message(
            "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709"
        )

    elif cmd == "coinflip":
        return with_embed(
            EmbedUtil.prep("Coinflip", choice(["**Heads**.", "**Tails**."]))
        )

    elif cmd == "8":
        return with_message(random_from_file("8ball"))

    elif cmd == "clapify":
        return with_message(" :clap: ".join(args))

    # elif cmd == "say":
    #     s = ""
    #     for arg in args:
    #        s += arg.replace("@everyone", "").replace(
    #            "@here", ""
    #        )  # prevent exploit
    #        s += " "
    #    return s

    elif cmd == "joke":
        return with_message(random_from_file("jokes"))

    elif cmd == "start-profiler":
        if message.author.id in UserUtil.admins():
            yappi.set_clock_type("wall")
            yappi.start()
            return with_message(
                "Started the profiler. Once you are done, run stop-profiler."
            )
        else:
            return with_message(":x: **You are not authorized to run this!**")

    elif cmd == "stop-profiler":
        if message.author.id in UserUtil.admins():
            yappi.stop()
            yappi.get_func_stats().print_all(open("profile.txt", "w"))
            return with_message("Saved profiler results to `profile.txt`.")
        else:
            return with_message(":x: **You are not authorized to run this!**")

    return with_message("EMPTY")
