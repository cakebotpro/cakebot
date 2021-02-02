/**
 * Cakebot - A fun and helpful Discord bot
 * Copyright (C) 2021-current year  Reece Dunham
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { sep, join } from "path"
import { readFileSync } from "fs"

const s = sep
const pkgDirs: string[] = __dirname.split(s)
// ugly solution to get the path of this file, but 3 directories up
// the current working directory might not be from the source code, but instead
// a tgz installed with npm
pkgDirs.pop()
pkgDirs.pop()
pkgDirs.pop()
export const pkgDir: string = pkgDirs.join(s)
export const CONTENT_FOLDER = join(pkgDir, `content`)

export const eightballs = readFileSync(`${CONTENT_FOLDER}/8ball.txt`).toString().split("\n")

export const jokes = readFileSync(`${CONTENT_FOLDER}/jokes.txt`).toString().split("\n")

export const usersWithTicketsOpen: string[] = []
