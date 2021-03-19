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
import type { Message, User } from "discord.js"
import { mkdirSync, readFileSync, statSync, writeFileSync } from "fs"
import { sep } from "path"
import random from "random"
import { usersWithTicketsOpen } from "./remote/runtime-data"
import type { Schema } from "./types"
import { error } from "../util/logging"
import { getConfig } from "./config"

/* eslint-disable promise/no-nesting */

export const dbPath = `${process.cwd()}${sep}database.json`

let cakeCooldowns: string[] = []

/**
 * Loads the database.
 * @see inMemoryDB
 */
export function loadDb(): Schema {
    try {
        statSync(dbPath)
    } catch (e) {
        // doesn't exist
        writeFileSync(dbPath, defaultData)
    }

    const instream = readFileSync(dbPath)

    return JSON.parse(instream.toString()) as Schema
}

const defaultData = JSON.stringify({
    users: {},
    servers: {},
})

/**
 * The active database.
 * This is openly readable and writable.
 */
export const inMemoryDB: Schema = loadDb()

export function addUserById(userId: string): void {
    inMemoryDB.users[userId] = {
        cakeCount: 0,
    }
}

export function addServerById(serverId: string): void {
    inMemoryDB.servers[serverId] = {
        prefix: getConfig().prefix,
    }
}

export async function createEvent({
    msg,
    message,
}: {
    msg: string
    message: Message
}): Promise<void> {
    const announcementMessage = await message.channel.send(msg)
    const server = inMemoryDB.servers[message.guild?.id || ""]
    server.activeEvent = {
        people: [message.author.id],
        reactionMessageId: announcementMessage.id,
    }
    inMemoryDB.servers[message.guild?.id || ""] = server
}

export function startEvent(message: Message): void {
    message.channel
        .send("Starting the event now!")
        .then(() => {
            const server = inMemoryDB.servers[message.guild?.id || ""]
            server.activeEvent?.people.forEach((person) => {
                // eslint-disable-next-line promise/no-nesting
                message.guild
                    ?.member(person)
                    ?.createDM()
                    .then((channel) => {
                        channel.send("An event you joined is starting now!")
                        return
                    })
                    .catch((e) => error(e))
            })
            server.activeEvent = undefined

            inMemoryDB.servers[message.guild?.id || ""] = server
            return
        })
        .catch((reason) => error(reason))
}

export async function createTicket({
    message,
    author,
}: {
    message: string
    author: User
}): Promise<void> {
    if (message.length >= 1000) {
        throw new Error("Message too large!")
    }

    if (usersWithTicketsOpen.includes(author.id)) {
        throw new Error(
            "You already have a ticket open! Please wait until it is resolved to open another."
        )
    }

    usersWithTicketsOpen.push(author.id)

    try {
        statSync("tickets")
    } catch (e) {
        mkdirSync("tickets")
    }

    const ticketId = random.int(1, 1_000_000)

    writeFileSync(
        `tickets/${ticketId}.txt`,
        `Author: ${author.username}#${author.discriminator}
Message: ${message}`
    )
}

export function commitCooldown(userId: string): void {
    cakeCooldowns.push(userId)
}

export function removeCooldown(userId: string): void {
    cakeCooldowns = cakeCooldowns.filter((item) => item !== userId)
}

export function getCooldowns(): string[] {
    return cakeCooldowns
}
