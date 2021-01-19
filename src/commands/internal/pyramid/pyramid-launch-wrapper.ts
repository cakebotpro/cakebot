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
import { start } from "../../../index"
import { defaultCommandsHookup } from "../../commands"
import Arrest from "./arrest"
import MuteAll from "./muteall"
import Pardon from "./pardon"

const ADMINS = [
    "411505437003743243",
    "497194854099451904",
    "617194842723975198",
    "701492075799117934",
    "506121585929748491",
]

// start with default commands hookup and a custom hookup that applies Pyramid server commands
start([
    defaultCommandsHookup,
    ({ commandRegistry }) => {
        commandRegistry.register(Arrest(ADMINS))
        commandRegistry.register(MuteAll(ADMINS))
        commandRegistry.register(Pardon(ADMINS))
    },
])
