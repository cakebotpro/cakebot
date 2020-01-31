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

# mypy: ignore_errors

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from os.path import exists
from os import getenv


engine = create_engine("sqlite:///cakebot.db" if getenv("TEST_ENV") is None else "sqlite:///testenv.db")
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()


class DiscordUser(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    cookie_count = Column(Integer, default=0)
    last_got_cookie_at = Column(DateTime())


def create():
    return Base.metadata.create_all(engine)


def get_user_by_id(id):
    query_result = session.query(DiscordUser).filter_by(id=id).first()

    if query_result is not None:
        return query_result

    new_query = DiscordUser(
        id=id,
        last_got_cookie_at=datetime(2015, 1, 1, 1, 1, 1, 1)
    )
    session.add(new_query)
    commit()

    return new_query


def commit():
    session.commit()


if not exists("cakebot.db"):
    create()
