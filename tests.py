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


import os
import unittest


class Tests(unittest.TestCase):
    def setUp(self):
        os.environ["TEST_ENV"] = "yes"

    def test_userutil(self):
        """Test cakebot.UserUtil"""

        from cakebot import UserUtil

        self.assertIsNotNone(UserUtil)
        self.assertIsNotNone(UserUtil.admins())
        self.assertIsInstance(UserUtil.admins(), list)

    def test_textcommandsutil(self):
        """Test cakebot.TextCommandsUtil"""

        from cakebot import TextCommandsUtil

        self.assertIsNotNone(TextCommandsUtil)
        self.assertIsInstance(TextCommandsUtil.common("jokes"), str)
        self.assertIsNone(TextCommandsUtil.noop())

    def test_get_mentioned_id(self):
        """Test cakebot.TextCommandsUtil.get_mentioned_id"""

        from cakebot.TextCommandsUtil import get_mentioned_id as gmId

        self.assertIsNotNone(gmId)
        self.assertEqual(
            gmId(["please", "find", "the", "id", "of", "<@!123456789>"]), 123456789
        )
        self.assertIsNone(gmId(["please", "find", "the", "id", "of", "nobody"]))
        self.assertIsNone(gmId(["<@!123>"]))

    def test_embedutil(self):
        """Test cakebot.EmbedUtil"""

        from cakebot import EmbedUtil

        self.assertIsNotNone(EmbedUtil)
        self.assertIsInstance(EmbedUtil.prep(title="a", description="b"), EmbedUtil.Embed)

    @unittest.skipUnless(os.getenv("CIRRUS_CI") is not None, "not in Cirrus CI")
    def test_database(self):
        """Test cakebot.Database"""

        from cakebot import Database

        Database.create()
        self.assertTrue(os.path.exists("cakebot.db"))
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


if __name__ == "__main__":
    unittest.main()
