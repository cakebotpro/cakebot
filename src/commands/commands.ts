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
import type { Message, MessageReaction, PartialUser, User } from "discord.js"
import type { ApplyHookup } from ".."
import Boomer from "./internal/boomer"
import Cake from "./internal/cake"
import Clapify from "./internal/clapify"
import Coinflip from "./internal/coinflip"
import Define from "./internal/define"
import * as Events from "./internal/events"
import EightBall from "./internal/eightball"
import Fact from "./internal/fact"
import Help from "./internal/help"
import Homepage from "./internal/homepage"
import Info from "./internal/info"
import Invite from "./internal/invite"
import Iss from "./internal/iss"
import Joke from "./internal/joke"
import Pi from "./internal/pi"
import Ping from "./internal/ping"
import Report from "./internal/report"
import Say from "./internal/say"
import Shutdown from "./internal/shutdown"
import Slots from "./internal/slots"
import Stars from "./internal/stars"
import Trump from "./internal/trump"

/**
 * A command that users can execute.
 */
export default interface Command {
    /**
     * The command's name.
     */
    name: string

    /**
     * A list of aliases that the command can also be used by.
     * @example
     * aliases: ["hi"], // If this command's name is set to 'hello', 'hi' will do the same thing!
     */
    aliases?: string[]

    /**
     * Called when the command is executed by a user.
     * @param args The arguments passed. This will always be a list of strings.
     * @param message The discord.js message object.
     * @return Nothing.
     */
    execute(args: readonly string[], message: Message): void
}

export const defaultCommands: Command[] = [
    Boomer,
    Cake,
    Clapify,
    Coinflip,
    Define,
    EightBall,
    Events.default,
    Fact,
    Help,
    Homepage,
    Info,
    Invite,
    Iss,
    Joke,
    Pi,
    Ping,
    Report,
    Say,
    Shutdown,
    Slots,
    Stars,
    Trump,
]

/**
 * A hookup that applies the bot's default commands.
 *
 * @param context The context.
 */
export const defaultCommandsHookup: ApplyHookup = (context) => {
    const { commandRegistry, botClient } = context

    defaultCommands.forEach((cmd) => commandRegistry.register(cmd))

    botClient.on(
        "messageReactionAdd",
        (reaction: MessageReaction, user: User | PartialUser) => {
            Events.handleReactionAdd(reaction, user)
        }
    )

    botClient.on(
        "messageReactionRemove",
        (reaction: MessageReaction, user: User | PartialUser) => {
            Events.handleReactionRemove(reaction, user)
        }
    )
}
