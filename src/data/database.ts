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
import { readFileSync, statSync, writeFile, writeFileSync } from "fs"
import path from "path"

const dbPath = `${process.cwd()}${path.sep}database.json`

export interface User {
    cakeCount: number
}

export interface Schema {
    users: {
        [userId: string]: User
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

export function getUserById(userId: string, useConfig?: () => Schema): User {
    const d = (useConfig || loadConfig)()

    if (!d.users[userId]) {
        addUserById(userId, d)
    }

    return d.users[userId]
}

export function save(data: Schema): void {
    writeFile(dbPath, JSON.stringify(data), (err) => {
        throw err
    })
}
