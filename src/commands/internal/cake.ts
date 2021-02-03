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

import type {User} from "discord.js"
import {addUserById, inMemoryDB} from "../../data/database"
import Command from "../commands"
import {makeError} from "../../util/constants"
import {cakebot} from "../../index";
import {MessageEmbed} from "discord.js";

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

            if (subcommand === "leaderboard") {
                const mappedData = Object
                    .keys(inMemoryDB.users)
                    .map(user => {
                        return {
                            id: user,
                            data: inMemoryDB.users[user]
                        }
                    })
                    .sort(user => user.data.cakeCount);

                const md = mappedData.map(data => {
                    const index = mappedData.indexOf(data);
                    if (index <= 10) {
                        const user = cakebot.users.cache.find(u => u.id == data.id)
                        return `${index + 1}. ${user?.tag ?? "Name#0000"} - ${data.data.cakeCount} cakes`;
                    } else {
                        return null;
                    }
                }).filter(item => item !== null);

                const executorIndex = mappedData.findIndex(u => u.id == message.author.id);

                if (executorIndex > 11) {
                    md.push(`${executorIndex + 1}. ${message.author.username} - ${getCount(message.author)} cakes`);
                }

                if (md.length == 0) {
                    md.push("There doesn't seem to be anybody on the leaderboard :(.");
                }

                const embed = new MessageEmbed()
                    .setColor(message.member?.displayColor ?? "#2196f3")
                    .setTimestamp(Date.now())
                    .setDescription(md.join("\n"))
                    .setAuthor("Leaderboard")

                message.channel.send(embed);
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
