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
import Command from "../commands"
import type {
    GuildMember,
    PartialUser,
    User,
    MessageReaction,
} from "discord.js"
import { makeError } from "../../util/constants"
import {
    addServerById,
    createEvent,
    inMemoryDB,
    startEvent,
} from "../../data/database"

const Events: Command = {
    name: "events",
    aliases: ["event"],
    execute(args, message) {
        if (!message.guild) {
            message.channel.send(makeError("Not in a server!"))
            return
        }

        if (args.length < 1) {
            message.channel.send(
                makeError(
                    `You didn't provide a subcommand! Please read the documentation on how to create and manage events.

If you want to join the event, just run the \`join\` subcommand!`
                )
            )
        }

        if (args[0] === "create") {
            if (!inMemoryDB.servers[message.guild.id]) {
                addServerById(message.guild.id)
            }

            if (args.length <= 2) {
                message.channel.send(
                    makeError(
                        "You need to specify an event name after `create`, e.g. 'Some cool event'."
                    )
                )
                return
            }

            if (inMemoryDB.servers[message.guild.id].activeEvent) {
                message.channel.send(
                    makeError("This server already has an active event!")
                )
                return
            }

            const author: GuildMember = message.guild.members.cache.get(
                message.author.id
            )!

            if (author.hasPermission("MANAGE_GUILD")) {
                createEvent({ msg: args.slice(1).join(" "), message })
                    .then(() => {
                        return
                    })
                    .catch((err) => {
                        message.channel.send(makeError(err))
                    })
                return
            }
        }

        if (args[0] === "start") {
            if (!inMemoryDB.servers[message.guild.id]) {
                addServerById(message.guild.id)
            }

            if (!inMemoryDB.servers[message.guild.id].activeEvent) {
                message.channel.send(
                    makeError("This server doesn't have an active event!")
                )
                return
            }

            const author: GuildMember = message.guild.members.cache.get(
                message.author.id
            )!

            if (author.hasPermission("MANAGE_GUILD")) {
                startEvent(message)
                return
            }
        }

        if (args[0] == "join") {
            if (!inMemoryDB.servers[message.guild.id]) {
                addServerById(message.guild.id)
            }

            const srv = inMemoryDB.servers[message.guild.id]

            if (!srv.activeEvent) {
                message.channel.send(
                    makeError("No event is currently running in this server!")
                )
                return
            }

            if (srv.activeEvent.people.includes(message.author.id)) {
                message.channel.send(
                    makeError(
                        "You are already scheduled to attend this event! To leave, use the `leave` subcommand."
                    )
                )
            }

            srv.activeEvent.people.push(message.author.id)
            inMemoryDB.servers[message.guild.id] = srv
            message.channel.send("Success! You are now a part of the event.")
        }

        if (args[0] == "leave") {
            if (!inMemoryDB.servers[message.guild.id]) {
                addServerById(message.guild.id)
            }

            const srv = inMemoryDB.servers[message.guild.id]

            if (!srv.activeEvent) {
                message.channel.send(
                    makeError("No event is currently running in this server!")
                )
                return
            }

            if (!srv.activeEvent.people.includes(message.author.id)) {
                message.channel.send(
                    makeError(
                        "You aren't already scheduled to attend this event! To join it, use the `join` subcommand."
                    )
                )
            }

            const newPeople: string[] = []
            srv.activeEvent.people.forEach((person) => {
                if (person !== message.author.id) {
                    newPeople.push(person)
                }
            })

            srv.activeEvent.people = newPeople
            inMemoryDB.servers[message.guild.id] = srv
            message.channel.send(
                "Success! You are no longer a part of the event."
            )
        }
    },
}

export function handleReactionAdd(
    m: MessageReaction,
    user: User | PartialUser
): void {
    if (!m.message.guild) {
        return
    }

    if (!inMemoryDB.servers[m.message.guild.id]) {
        addServerById(m.message.guild.id)
    }

    const srv = inMemoryDB.servers[m.message.guild.id]

    if (!srv.activeEvent) {
        return
    }

    if (srv.activeEvent.people.includes(user.id)) {
        return
    }

    srv.activeEvent.people.push(user.id)
    inMemoryDB.servers[m.message.guild.id] = srv
}

export function handleReactionRemove(
    m: MessageReaction,
    user: User | PartialUser
): void {
    if (!m.message.guild) {
        return
    }

    const srv = inMemoryDB.servers[m.message.guild.id]

    if (!srv.activeEvent) {
        return
    }

    if (srv.activeEvent.people.includes(user.id)) {
        const newUsers: string[] = []

        srv.activeEvent.people.forEach((person) => {
            if (person !== user.id) {
                newUsers.push(user.id)
            }
        })

        srv.activeEvent.people = newUsers
        inMemoryDB.servers[m.message.guild.id] = srv
    }
}

export default Events
