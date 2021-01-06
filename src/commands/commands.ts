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

import { Message } from "discord.js"
import Registry from "./registry"
import logger from "../util/logging"

import Help from "./internal/help"
import Ping from "./internal/ping"
import Boomer from "./internal/boomer"
import EightBall from "./internal/eightball"
import Joke from "./internal/joke"
import Pi from "./internal/pi"
import Clapify from "./internal/clapify"

export default interface Command {
    name: string
    aliases?: string[]
    execute(args: readonly string[], message: Message): void
}

const internalCommands: Command[] = [
    Help,
    Ping,
    Boomer,
    EightBall,
    Joke,
    Pi,
    Clapify,
]

export function registerInternalCommands(
    commandRegistry: Registry<Command>
): void {
    internalCommands.forEach((cmd) => {
        commandRegistry.register(cmd)
        logger.debug(`Loaded command '${cmd.name}'.`)
    })
}
