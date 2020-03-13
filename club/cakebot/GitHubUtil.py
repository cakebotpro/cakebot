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

issue_template = """\
## Support Ticket

> Filed by {str(message.author)}

### Message:

`{0}`

##### Powered by Cakebot | https://cakebot.club"
"""


async def report(s, g, args, message):
    repo = g.get_repo("cakebotpro/cakebot")
    f = " ".join(args)
    if f == "" or f == " ":
        return await s(":x: **I can't report nothing!**")
    repo.create_issue(
        title="Support ticket #" + str(randint(0, 100000)),
        body=issue_template.format(f),
        labels=[repo.get_label("ticket")],
    )
    return await s(":white_check_mark: **Our team has been notified.**")
