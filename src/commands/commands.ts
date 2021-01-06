import { Message } from "discord.js"
import Registry from "./registry"
import logger from "../util/logging"

import Help from "./internal/help"
import Ping from "./internal/ping"
import Boomer from "./internal/boomer"
import EightBall from "./internal/eightball"
import Joke from "./internal/joke"

export default interface Command {
    name: string
    aliases?: string[]
    execute(args: readonly string[], message: Message): void
}

const internalCommands: Command[] = [Help, Ping, Boomer, EightBall, Joke]

export function registerInternalCommands(
    commandRegistry: Registry<Command>
): void {
    internalCommands.forEach((cmd) => {
        commandRegistry.register(cmd)
        logger.debug(`Loaded command '${cmd.name}'.`)
    })
}
