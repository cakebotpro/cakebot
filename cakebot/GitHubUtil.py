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

from random import randint
from typing import Any, List

from discord import Message
from github import Github

issue_template = """\
## Support Ticket

> Filed by {0}

### Message:

`{1}`

##### Powered by Cakebot | https://cakebot.club"
"""


async def report(s: Any, g: Github, args: List[str], message: Message):
    """Reports an error to the GitHub page."""

    repo = g.get_repo("cakebotpro/cakebot")
    f = " ".join(args)
    repo.create_issue(
        title="Support ticket #" + str(randint(0, 100000)),
        body=issue_template.format(str(message.author), f),
        labels=[repo.get_label("ticket")],
    )
    return await s(":white_check_mark: **Our team has been notified.**")
