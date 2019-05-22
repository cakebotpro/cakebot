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

import io

class AbstractFile:
    # init class
    def __init__(self, name):
        self.name = name

    # override __str__ method
    def __str__(self):
        return self.name

    # get the name
    def get_name(self):
        return self.__str__()

    # io stuff
    def wrap(self):
        return open(self.get_name(), mode="a")


class FileHandler:
    # init class
    def __init__(self, abstractFile):
        self.cache = []
        if type(abstractFile) != AbstractFile:
            raise TypeError("'abstractFile' param must be instance of AbstractFile!")
        else:
            self.theFile = abstractFile

    def get_file(self):
        return self.theFile

    def get_file_name(self):
        return self.get_file().get_name()

    def refresh(self):
        with open(self.get_file_name(), mode="r") as filehandler:
            if not type(filehandler) is io.TextIOWrapper:
                raise TypeError("Could not create a TextIOWrapper for the file!")
            else:
                self.cache = filehandler.readlines()
                # strip newlines
                for h, g in enumerate(self.cache):
                    self.cache[h] = self.cache[h].replace("\n", "")

    def get_cache(self):
        return self.cache
