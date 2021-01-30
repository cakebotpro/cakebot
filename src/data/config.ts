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
import { debug, error, info } from "../util/logging"

/**
 * A model for an object containing the possible configuration values.
 */
export interface Configuration {
    discordToken: string
    prefix: string
    status: string
    wordsapiToken?: string
    githubToken?: string
    debug: boolean
    bannedUserIds: string[]
    adminUserIds: string[]
}

/**
 * A model for all the possible and required environment variables.
 */
export interface ExpectedEnvironment {
    DISCORD_TOKEN: string
    BOT_PREFIX?: string
    BOT_STATUS?: string
    DEBUG?: string
    WORDSAPI_TOKEN?: string
    GITHUB_TOKEN?: string
    BANNED_IDS?: string
    ADMIN_IDS?: string
}

// avoid recalculating these every time getConfig is called
let bannedUsersCache: string[] | undefined = undefined
let adminUsersCache: string[] | undefined = undefined

/**
 * Returns if the value passed is a string representation of true.
 * @param v The string to check.
 * @returns If the string equals "true".
 * @example
 * isTruthish(undefined) // false
 * isTruthish(true) // false
 * isTruthish("true") // true
 */
export function isTruthish(v?: string): boolean {
    if (!v) {
        return false
    }

    return v.toLowerCase() === "true"
}

/**
 * Parses the banned users and admin users environment variables, and returns a list of user IDs as strings.
 * @param typeName The display name for the type of the list (e.g. "banned users").
 * @param v The value of the environment variable.
 * @returns The banned IDs list.
 */
function parseUserList(typeName: string, v?: string): string[] {
    if (typeName === "admin users" && adminUsersCache !== undefined) {
        return adminUsersCache
    }

    if (typeName === "banned users" && bannedUsersCache !== undefined) {
        return bannedUsersCache
    }

    if (!v) {
        return []
    }

    const ids: string[] = []

    const s = v.split(",")
    s.forEach(function eachUser(pid): void {
        ids.push(pid)
        debug(`Added ID ${pid} to the ${typeName} list.`, true)
    })

    if (typeName === "admin users") {
        adminUsersCache = ids
    } else {
        bannedUsersCache = ids
    }

    return ids
}

/**
 * Gets the configuration from the environment variables.
 * @returns The configuration.
 * @throws Error If the configuration is invalid.
 * @see validateConfig
 */
export function getConfig(): Configuration {
    const env = (process.env as unknown) as ExpectedEnvironment

    const config = {
        discordToken: env.DISCORD_TOKEN,
        wordsapiToken: env.WORDSAPI_TOKEN,
        githubToken: env.GITHUB_TOKEN,
        debug: isTruthish(env.DEBUG),
        bannedUserIds: parseUserList("banned users", env.BANNED_IDS),
        adminUserIds: parseUserList("admin users", env.ADMIN_IDS),
        prefix: env.BOT_PREFIX || "-",
        status: env.BOT_STATUS || "Run (PREFIX)help",
    }

    if (validateConfig(config)) {
        return config
    }

    error("No Discord token specified!")
    error(
        `You need to put it into \`process.env\` in your launcher, called 'DISCORD_TOKEN'!`
    )
    info(
        "See https://cakebot.club/docs/selfhosting/environment-variables for more info."
    )
    throw new Error("Failing due to invalid configuration.")
}

/**
 * Validates the configuration object for any errors.
 * @param config The configuration to validate.
 * @returns If the config is valid (true), or has errors (false).
 */
export function validateConfig(config: Configuration): boolean {
    // Checks if the Discord token is null or undefined.
    return !!config.discordToken
}
