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
import { info } from "../../util/logging"
import { inMemoryDB } from "../database"
import chalk from "chalk"
import { getConfig } from "../config"

export const CURRENT_PATCH_LEVEL = 1

export function applyPatch(patchId: number): void {
    info(
        chalk`Applying patch {green patch${patchId.toString()}} to the database.`
    )
    switch (patchId) {
        // Add version to the DB
        case 0:
            inMemoryDB.version = 0
            break
        // Add per-server prefixes
        case 1:
            inMemoryDB.version = 1
            Object.keys(inMemoryDB.servers).forEach((serverId) => {
                inMemoryDB.servers[serverId].prefix = getConfig().prefix
            })
            break
    }
}

/**
 * Ensures everything is up to date.
 */
export default function update(): void {
    if (!inMemoryDB.version) {
        applyPatch(0)
    }

    while (inMemoryDB.version! < CURRENT_PATCH_LEVEL) {
        applyPatch(inMemoryDB.version! + 1)
        continue
    }
}
