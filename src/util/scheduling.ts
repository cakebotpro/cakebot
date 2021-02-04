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
import { writeFileSync } from "fs"
import { commitLeaderboardData, dbPath, inMemoryDB } from "../data/database"
import type { LeaderboardEntry } from "../data/types"
import type { Client } from "discord.js"
import { warn } from "./logging"

function callback(): void {
    writeFileSync(dbPath, JSON.stringify(inMemoryDB))
}

export function scheduleTasks(botClient: Client): void {
    setInterval(() => callback(), 150_000)
    setInterval(() => {
        recalculateLeaderboard(botClient)
            .catch((e) => warn(e))
    }, 900_000)
    // also first time
    recalculateLeaderboard(botClient)
        .catch((e) => warn(e))
}

export async function recalculateLeaderboard(botClient: Client): Promise<void> {
    const lb: LeaderboardEntry[] = []

    const mappedData = Object.keys(inMemoryDB.users)
        .map((user) => {
            return {
                id: user,
                data: inMemoryDB.users[user],
            }
        })
        .sort((userOne, userTwo) => {
            return userOne.data.cakeCount - userTwo.data.cakeCount
        })

    let i = 0

    while (i < 10) {
        const data = mappedData[i]

        if (data) {
            const user = await botClient.users.fetch(data.id, true)
            if (data.data.cakeCount >= 1) {
                lb.push({ name: user?.tag ?? "", cakes: data.data.cakeCount })
            }
        }

        i += 1
    }

    commitLeaderboardData(lb)
}
