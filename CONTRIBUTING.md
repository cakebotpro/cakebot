# Contributing

Hello and welcome to Cakebot!  Before you open a pull request, please take a look over this guide.

## Development

### New Python Modules

If adding new `.py` files, please add the following copyright header to the top:

```python
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
```

This is *required* by the license this repository is under.

### Installing Dependencies

Please run this in a terminal:
```none
python3.6 -m pip install --upgrade --user --extra-index-url 'https://cakebot.mycloudrepo.io/public/repositories/py' -r requirements.txt
```

### Starting The Bot

The bot is built to work on our server, and because of that, some paths/files may be wrong on your computer.

#### GitHub

You will need to comment out the `+report` command and its GitHub API wrapper instance, as we aren't publishing our personal
access token.

#### Discord

You will need to create your own bot and suply a token if you want to run it.

### Python Version

Please use Python `v3.6.x`.
