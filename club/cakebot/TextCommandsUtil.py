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
    return choice(open("content/" + n + ".txt", mode="r").readlines())


def clapify(args):
    s = ""
    for arg in args:
        if s == "":
            s = str(arg + " ")
        else:
            s += str(":clap: " + arg + " ")
    return s


def noop():
    return


def get_mentioned_id(message_contents):
    for item in message_contents:
        if item.startswith("<@!") and item.endswith(">"):
            base = item
            # strip out the divider chars
            base = base.replace("<@!", "")
            base = base.replace(">", "")
            return int(base)
        try:
            if int(item) > 100000:
                return int(item)
        except ValueError:
            noop()
    return None


async def define(args, s):
    c = ""
    if len(args) < 1:
        return await s(":x: *You need to specify a word!*")
    if len(args) > 1:
        for b, h in enumerate(args):
            c = str(c + args[b] + "%20")
    else:
        c = args[0]
    sm = BeautifulSoup(
        get(f"https://www.merriam-webster.com/dictionary/{c}").content,
        "html.parser"
    ).find(
        "span", attrs={"class": "dtText"}
    ).text
    return await s(c + sm)


data_template = """\
***{message.guild.name}***
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

issue_template = """\
## Support Ticket

> Filed by {str(message.author)}

### Message:

`{0}`

##### Powered by Cakebot | https://cakebot.club"
"""
