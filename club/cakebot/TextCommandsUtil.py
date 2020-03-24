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
from bs4 import BeautifulSoup
from requests import get


def common(n):
    """Load a content file (used a lot)."""
    fileobj = open("content/" + n + ".txt", mode="r")
    lines = fileobj.readlines()
    fileobj.close()
    return choice(lines)


def noop():
    """Literally just do nothing."""
    return


def get_mentioned_id(args):
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


def define(args):
    """Defines a word."""
    c = ""
    if len(args) < 1:
        return ":x: *You need to specify a word!*"
    if len(args) > 1:
        for b, h in enumerate(args):
            c = str(c + args[b] + "%20")
    else:
        c = args[0]
    sm = (
        BeautifulSoup(
            get(f"https://www.merriam-webster.com/dictionary/{c}").content,
            "html.parser",
        )
        .find("span", attrs={"class": "dtText"})
        .text
    )
    return " ".join([c, sm])


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


def handle_common_commands(message, args, cmd):
    """Handles certain simple commands."""
    if cmd == "define":
        return define(args)

    elif cmd == "pi":
        return "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709"

    elif cmd == "coinflip":
        return choice(["**Heads**.", "**Tails**."])

    elif cmd == "8":
        return common("8ball")

    elif cmd == "clapify":
        return " :clap: ".join(args)

    return None
