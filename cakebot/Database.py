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

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///cakebot.db")
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()


class DiscordUser(Base):  # type: ignore
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    cookie_count = Column(Integer, default=0)
    last_got_cookie_at = Column(DateTime())

    def __repr__(self):
        return "<DiscordUser {0} {1}>".format(self.id, self.cookie_count)


def create():
    """Creates the database."""
    return Base.metadata.create_all(engine)


def get_user_by_id(id: int) -> DiscordUser:
    """
    Finds a user in the database from their Discord ID,
    and creates an entry if they don't exist yet.
    """

    query_result = session.query(DiscordUser).filter_by(id=id).first()

    if query_result is not None:
        return query_result

    new_query = DiscordUser(
        id=id, last_got_cookie_at=datetime(2015, 1, 1, 1, 1, 1, 1)
    )
    session.add(new_query)
    commit()

    return new_query


def commit():
    """Commits all changes to the database."""
    session.commit()
