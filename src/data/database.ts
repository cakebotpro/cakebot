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
import { User } from "discord.js"
import { mkdirSync, readFileSync, statSync, writeFileSync } from "fs"
import path from "path"
import random from "random"
import { usersWithTicketsOpen } from "./remote/runtime-data"

const dbPath = `${process.cwd()}${path.sep}database.json`

export interface CBUser {
    cakeCount: number
}

export interface Schema {
    users: {
        [userId: string]: CBUser
    }
    servers: {
        [serverId: string]: Record<string, never>
    }
}

const defaultData = JSON.stringify({
    users: {},
    servers: {},
})

export function runDatabasePreChecks(): void {
    try {
        statSync(dbPath)
    } catch (e) {
        // doesn't exist
        writeFileSync(dbPath, defaultData)
    }
}

function addUserById(userId: string, data: Schema): void {
    data.users[userId] = {
        cakeCount: 0,
    }
    save(data)
}

export function loadConfig(): Schema {
    const instream = readFileSync(dbPath)

    return JSON.parse(instream.toString()) as Schema
}

export function getUserById(userId: string, useConfig?: () => Schema): CBUser {
    const d = (useConfig || loadConfig)()

    if (!d.users[userId]) {
        addUserById(userId, d)
    }

    return d.users[userId]
}

export function createTicket({
    message,
    author,
}: {
    message: string
    author: User
}): Promise<void> {
    return new Promise<void>((resolve, reject) => {
        if (message.length >= 1000) {
            reject("Message too large!")
            return
        }

        if (usersWithTicketsOpen.includes(author.id)) {
            reject(
                "You already have a ticket open! Please wait until it is resolved to open another."
            )
            return
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
            `Author: ${author.username}

Message: ${message}`
        )

        resolve()
    })
}

export function save(data: Schema): void {
    writeFileSync(dbPath, JSON.stringify(data))
}
