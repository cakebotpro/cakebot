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

import type { User } from "discord.js"
import { addUserById, getLeaderboard, inMemoryDB } from "../../data/database"
import Command from "../commands"
import { makeError } from "../../util/constants"
import createEmbed from "../../util/embeds"

export function getCount(user: User): number {
    if (!inMemoryDB.users[user.id]) {
        addUserById(user.id)
    }

    return inMemoryDB.users[user.id].cakeCount
}

function give(to: User): void {
    if (!inMemoryDB.users[to.id]) {
        addUserById(to.id)
    }

    inMemoryDB.users[to.id].cakeCount += 1
}

const Cake: Command = {
    name: "cake",
    aliases: ["cakes"],
    execute(args, message) {
        const subcommand = args[0]

        if (subcommand) {
            if (subcommand === "count") {
                let user = message.mentions.users.first()

                if (!user) {
                    user = message.author
                }

                message.channel.send(
                    `${user?.username} has ${getCount(user)} cakes.`
                )
            }

            if (subcommand === "give") {
                const user = message.mentions.users.first()

                if (!user) {
                    message.channel.send(
                        makeError(
                            "I don't know who to give a cake to, please **mention them**."
                        )
                    )
                    return
                }

                give(user)

                message.channel.send(
                    `Done! ${user?.username} now has ${getCount(user)} cakes.`
                )
            }

            if (subcommand === "leaderboard" || subcommand === "lb") {
                if (getLeaderboard().length == 0) {
                    message.channel.send(
                        makeError(
                            "There doesn't seem to be anybody on the leaderboard, or it hasn't been calculated yet :sad:"
                        )
                    )
                    return
                }

                message.channel.send(
                    createEmbed(
                        "Leaderboard",
                        "The people with the most cakes!",
                        getLeaderboard().reverse().map((ent) => ({
                            name: ent.name,
                            value: `${ent.cakes} cakes.`,
                            inline: false,
                        }))
                    )
                )
            }
        } else {
            message.channel.send(
                makeError(
                    "I expected a subcommand. Try `+cake` `give`, `count`, or `leaderboard`."
                )
            )
        }
    },
}

export default Cake
