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
import { Client, Message } from "discord.js"
import "source-map-support/register"
import Command, { registerInternalCommands } from "./commands/commands"
import Registry from "./commands/registry"
import { getConfig } from "./data/config"
import { Trace } from "./data/tracing"
import logger from "./util/logging"

process.on("unhandledRejection", (e) => {
    throw e
})

const options = {
    shards: "auto",
    presence: {
        activity: {
            name: "Run +help | EARLY BETA OF CAKEBOT 2!",
            type: "PLAYING",
        },
    },
}

// string neq "auto" literal for some reason
// todo: why is record casting a thing
const cakebot = new Client(
    options as Record<string, string | Record<string, Record<string, string>>>
)

const commandRegistry = new Registry<Command>()

cakebot.on("ready", function cakebotReadyCallback() {
    logger.info("Completed setup, bot is now ready on Discord!")
})

cakebot.on("message", function cakebotMessageCallback(message: Message) {
    if (message.author.bot) {
        return
    }

    const argString = message.content
    const argArray = argString.split(" ")

    if (!argArray[0].startsWith("-")) {
        return
    }

    const command = argArray[0].replace("-", "").toLowerCase()

    // remove command
    let args = [...argArray]
    args = args.reverse()
    args.pop()
    args = args.reverse()

    const trace = new Trace(command, args, message.author.toString())

    try {
        let exe = commandRegistry.find("name", command)

        if (exe === null) {
            // second pass for alias checking
            exe = commandRegistry.find("aliases", command)
        }

        if (exe === null) {
            return
        }

        logger.debug(`Command trace: ${trace}`)
        exe?.execute.call(exe, args, message)
    } catch (e) {
        logger.error("An error occured during runtime.")
        throw e
    }
})

export default function start(): void {
    logger.info("Starting!")
    registerInternalCommands(commandRegistry)
    cakebot.login(getConfig().discordToken)
}
