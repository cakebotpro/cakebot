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
import logger from "../util/logging"

export interface Configuration {
    discordToken: string
    prefix: string
    status: string
    wordsapiToken?: string
    githubToken?: string
    debug: boolean
    bannedUserIds: string[]
}

export interface ExpectedEnvironment {
    DISCORD_TOKEN: string
    BOT_PREFIX?: string
    BOT_STATUS?: string
    DEBUG?: string
    WORDSAPI_TOKEN?: string
    GITHUB_TOKEN?: string
    BANNED_IDS?: string
}

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
 * Parses the banned users list environment variable, and returns a list of banned user IDs as strings.
 * @param v The value of the environment variable.
 * @returns The banned IDs list.
 */
function parseBannedUserList(v?: string): string[] {
    if (!v) {
        return []
    }

    const ids: string[] = []

    const s = v.split(",")
    s.forEach(function eachBannedUser(pid): void {
        ids.push(pid)
        logger.debug(`Added ID ${pid} to the ban list.`)
    })

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
        bannedUserIds: parseBannedUserList(env.BANNED_IDS),
        prefix: env.BOT_PREFIX || "-",
        status: env.BOT_STATUS || "Run (PREFIX)help",
    }

    if (validateConfig(config)) {
        return config
    }

    logger.error("No Discord token specified!")
    logger.error(
        `You need to put it in the .env file, with the variable being called 'DISCORD_TOKEN'!`
    )
    logger.info("See the documentation for more info.")
    throw new Error("Failing due to invalid configuration.")
}

/**
 * Validates the configuration object for any errors.
 *
 * @param config The configuration to validate.
 * @returns If the config has no errors (true), or has errors (false).
 */
export function validateConfig(config: Configuration): boolean {
    return !!config.discordToken
}
