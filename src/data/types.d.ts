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
    activeEvent?: CBEvent
}

/**
 * The primary database schema.
 */
export interface Schema {
    users: {
        [userId: string]: CBUser
    }
    servers: {
        [serverId: string]: CBServer
    }
}
