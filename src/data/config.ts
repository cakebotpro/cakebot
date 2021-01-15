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
    bannedUserIds: number[]
    googleMapsApiKey?: string
}

export interface ExpectedEnvironment {
    DISCORD_TOKEN: string
    BOT_PREFIX?: string
    BOT_STATUS?: string
    DEBUG?: string
    WORDSAPI_TOKEN?: string
    GITHUB_TOKEN?: string
    BANNED_IDS?: string
    GOOGLE_MAPS_API_KEY?: string
}

/**
 * Returns if the value passed is a string representation of true.
 *
 * @param v The string to check.
 * @returns If the string equals "true".
 */
function isTruthish(v?: string): boolean {
    if (!v) {
        return false
    }

    return v.toLowerCase() === "true"
}

function parseCommaList(v?: string): number[] {
    if (!v) {
        return []
    }

    const ids: number[] = []

    const s = v.split(",")
    s.forEach((pid) => {
        try {
            const i = Number.parseInt(pid)
            ids.push(i)
            logger.debug(`Added ID ${i.toString()} to the ban list.`)
        } catch (e) {
            // noop
        }
    })

    return ids
}

export function getConfig(): Configuration {
    const env = (process.env as unknown) as ExpectedEnvironment

    const config = {
        discordToken: env.DISCORD_TOKEN,
        wordsapiToken: env.WORDSAPI_TOKEN,
        githubToken: env.GITHUB_TOKEN,
        debug: isTruthish(env.DEBUG),
        bannedUserIds: parseCommaList(env.BANNED_IDS),
        googleMapsApiKey: env.GOOGLE_MAPS_API_KEY,
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
    process.exit(1)
}

/**
 * Validates the configuration object for any errors.
 *
 * @param config The configuration to validate.
 * @returns If the config has no errors (true), or has errors (false).
 */
export function validateConfig(config: Configuration): boolean {
    // don't run this validation when running `yarn test`
    if (process.env.IS_IN_JEST === "true") {
        return true
    }

    return !!config.discordToken
}
