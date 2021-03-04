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

/**
 * A Cakebot user.
 */
export interface CBUser {
    /**
     * The number of cakes that the user has.
     */
    cakeCount: number

    /**
     * Custom server only.
     */
    nonArrestRoles?: string[]
}

/**
 * A Cakebot event.
 */
export interface CBEvent {
    /**
     * A list of user IDs that have RSVP'd.
     */
    people: string[]

    /**
     * The ID of the message to react to in order to RSVP.
     */
    reactionMessageId: string
}

/**
 * A Cakebot Discord server as a database entry.
 */
export interface CBServer {
    prefix: string
    activeEvent?: CBEvent
}

/**
 * The primary database schema.
 */
export interface Schema {
    version?: number
    users: {
        [userId: string]: CBUser
    }
    servers: {
        [serverId: string]: CBServer
    }
}

/**
 * An entry on the most cakes leaderboard.
 */
export interface LeaderboardEntry {
    name: string
    cakes: number
}

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
