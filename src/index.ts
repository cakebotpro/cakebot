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
import "source-map-support/register"
import { Client, Message } from "discord.js"
import Registry from "./commands/registry"
import { getConfig } from "./data/config"
import * as Database from "./data/database"
import "./data/remote/runtime-data"
import Trace from "./data/tracing"
import { banner } from "./util/constants"
import { debug, error, info, warn } from "./util/logging"
import { dbPath, inMemoryDB } from "./data/database"
import { writeFileSync } from "fs"
import { schedulePeriodicDataSaves } from "./util/scheduling"

const CATCH_ERRORS = ["uncaughtException", "unhandledRejection"]
CATCH_ERRORS.forEach((errorName: string) => {
    process.on(errorName, function warnUnhandled(e): void {
        warn(e)
    })
})

/**
 * If this becomes true at any point,
 * we stop all functionality and attempt to perform last minute cleanup.
 * @readonly
 */
export let isShuttingDown = false

const settings = getConfig()

const options = {
    shards: "auto",
    presence: {
        activity: {
            name: settings.status.replace("(PREFIX)", settings.prefix),
            type: "PLAYING",
        },
    },
}

Database.loadDb()

const cakebot = new Client(
    options as Record<string, string | Record<string, Record<string, string>>>
)

const commandRegistry = new Registry()

cakebot.on("ready", function cakebotReadyCallback() {
    info("Completed setup, bot is now ready on Discord!")
})

cakebot.on("message", function cakebotMessageCallback(message: Message) {
    if (message.author.bot || isShuttingDown) {
        return
    }

    const argString = message.content
    const argArray = argString.split(" ")

    if (!argArray[0].startsWith(settings.prefix)) {
        return
    }

    if (getConfig().bannedUserIds.includes(message.author.id)) {
        message.channel.send(
            "**You have been banned from using the bot!** This typically happens because you abused a feature or caused a big problem for us."
        )
        return
    }

    const command = argArray[0].replace(settings.prefix, "").toLowerCase()

    let args = [...argArray]
    // pop first arg since it is the command
    args = args.reverse()
    args.pop()
    args = args.reverse()

    const trace = new Trace(command, args, message.author.tag)

    try {
        let exe = commandRegistry.find("name", command)

        if (exe === null) {
            // second pass for alias checking
            exe = commandRegistry.find("aliases", command)
        }

        if (exe === null) {
            return
        }

        debug(`Command trace: ${trace}`)
        exe.execute.call(exe, args, message)
    } catch (e) {
        error("An error occured during runtime.")
        warn(`Command trace: ${trace}`)
        error(e)
    }
})

/**
 * A method which accepts context details and applies whatever changes it needs to.
 */
export type ApplyHookup = (context: {
    commandRegistry: Registry
    botClient: Client
}) => void

/**
 * This should be implemnted in your launch script.
 *
 * @param applyHookups A list of hookups to apply.
 * @see ApplyHookup
 */
export function start(applyHookups: ApplyHookup | ApplyHookup[]): void {
    console.log(banner)
    info("Starting!")

    schedulePeriodicDataSaves()

    const context = { commandRegistry, botClient: cakebot }

    if (!applyHookups) {
        error(
            "No hookups have been specified, so if we launched, the bot would not do anything."
        )
        error("Aborting. Please see the docs for more information.")
        process.exit(1)
    }

    if (Array.isArray(applyHookups)) {
        applyHookups.forEach((hookup) => {
            hookup.call(hookup, context)
        })
    } else {
        applyHookups.call(applyHookups, context)
    }

    cakebot.login(getConfig().discordToken)
}

export function shutdown(): void {
    isShuttingDown = true
    writeFileSync(dbPath, JSON.stringify(inMemoryDB))
    process.exit(0)
}
