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


import unittest
import os


class Tests(unittest.TestCase):
    def setUp(self):
        os.environ["TEST_ENV"] = "yes"
        if os.path.exists("testenv.db"):
            os.remove("testenv.db")

    def test_userutil(self):
        """Test club.cakebot.UserUtil"""

        from club.cakebot import UserUtil

        self.assertIsNotNone(UserUtil)
        self.assertIsNotNone(UserUtil.admins())
        self.assertIsNotNone(UserUtil.contributors())
        self.assertIsInstance(UserUtil.admins(), list)
        self.assertIsInstance(UserUtil.contributors(), list)

    def test_textcommandsutil(self):
        """Test club.cakebot.TextCommandsUtil"""

        from club.cakebot import TextCommandsUtil

        self.assertIsNotNone(TextCommandsUtil)
        self.assertIsInstance(TextCommandsUtil.common("jokes"), str)
        self.assertIsNone(TextCommandsUtil.noop())

    def test_get_mentioned_id(self):
        """Test club.cakebot.TextCommandsUtil.get_mentioned_id"""

        from club.cakebot.TextCommandsUtil import get_mentioned_id as gmId

        self.assertIsNotNone(gmId)
        self.assertEqual(
            gmId(["please", "find", "the", "id", "of", "<@!123456789>"]), 123456789
        )
        self.assertIsNone(gmId(["please", "find", "the", "id", "of", "nobody"]))
        self.assertIsNone(gmId(["<@!123>"]))

    def test_embedutil(self):
        """Test club.cakebot.EmbedUtil"""

        from club.cakebot import EmbedUtil

        self.assertIsNotNone(EmbedUtil)
        self.assertIsInstance(EmbedUtil.prep(title="a", description="b"), EmbedUtil.Embed)

    def test_database(self):
        """Test club.cakebot.Database"""

        from club.cakebot import Database

        Database.create()
        self.assertTrue(os.path.exists("testenv.db"))
        self.assertIsNotNone(Database.DiscordUser)

        # it shouldn't have this entry yet
        self.assertEqual(
            Database.session.query(Database.DiscordUser).filter_by(id=5).all(), []
        )

        # create it
        self.assertIsNotNone(Database.get_user_by_id(5))

        # now check again
        self.assertNotEqual(
            Database.session.query(Database.DiscordUser).filter_by(id=5).all(), []
        )
        # and make sure its not None
        self.assertIsNotNone(
            Database.session.query(Database.DiscordUser).filter_by(id=5).all()
        )

        # lastly, check for prod db
        if os.getenv("CI") is not None:
            self.assertFalse(os.path.exists("cakebot.db"))


if __name__ == "__main__":
    unittest.main()
