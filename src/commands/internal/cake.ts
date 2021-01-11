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

import { User } from "discord.js"
import { getUserById, loadConfig, save, Schema } from "../../data/database"
import Command from "../commands"

function getCount(user: User): number {
    const u = getUserById(user.id.toString())
    return u.cakeCount
}

function give(to: User): void {
    const conf = loadConfig()

    const u = getUserById(to.id.toString(), function useConfig(): Schema {
        return conf
    })

    u.cakeCount += 1

    save(conf)
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
                        "I don't know who to give a cake to, please **mention them**."
                    )
                    return
                }

                give(user)

                message.channel.send(
                    `Done! ${user?.username} now has ${getCount(user)} cakes.`
                )
            }
        } else {
            message.channel.send(
                "I expected a subcommand. Try `+cake` `give`, `count`, or `leaderboard`."
            )
        }
    },
}

export default Cake
