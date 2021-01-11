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
import logger from "../util/logging"
import Boomer from "./internal/boomer"
import Cake from "./internal/cake"
import Clapify from "./internal/clapify"
import Coinflip from "./internal/coinflip"
import Define from "./internal/define"
import EightBall from "./internal/eightball"
import Fact from "./internal/fact"
import Help from "./internal/help"
import Homepage from "./internal/homepage"
import Joke from "./internal/joke"
import Pi from "./internal/pi"
import Ping from "./internal/ping"
import Slots from "./internal/slots"
import Stars from "./internal/stars"
import Registry from "./registry"
// import Iss from "./internal/iss"

export default interface Command {
    name: string
    aliases?: string[]
    execute(args: readonly string[], message: Message): void
}

const internalCommands: Command[] = [
    Boomer,
    Cake,
    Clapify,
    Coinflip,
    Define,
    EightBall,
    Fact,
    Help,
    Homepage,
    Joke,
    Pi,
    Ping,
    Slots,
    // todo: get billing set up for gmaps
    // Iss,
    Stars,
]

export function registerInternalCommands(
    commandRegistry: Registry<Command>
): void {
    internalCommands.forEach((cmd) => {
        commandRegistry.register(cmd)
        logger.debug(`Loaded command '${cmd.name}'.`)
    })
}
