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
