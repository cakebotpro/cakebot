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
import { warn } from "../../../util/logging"
import Command from "../../commands"
import { addUserById, inMemoryDB } from "../../../data/database"
import { makeError } from "../../../util/constants"

const Pardon = (admins: readonly string[]): Command => ({
    name: "pardon",
    aliases: ["uncancel"],
    execute(args, message) {
        const { guild } = message

        if (guild?.id === "702175596838649937") {
            const targetUser: User | undefined = message.mentions.users.first()

            if (!admins.includes(message.author.id)) {
                message.channel.send(makeError("You can't do that!!"))
                return
            }

            if (targetUser) {
                if (!inMemoryDB.users[targetUser.id]) {
                    addUserById(targetUser.id)
                }

                const actualUser = guild.member(targetUser)
                message.channel.send(
                    "Understood. Please allow a few seconds for pardoning to be executed."
                )

                actualUser?.roles.cache.each((value) => {
                    actualUser.roles.remove(value).catch((e) => {
                        warn(e)
                    })
                })

                if (inMemoryDB.users[targetUser.id].nonArrestRoles) {
                    inMemoryDB.users[targetUser.id].nonArrestRoles?.forEach(
                        (nonArrestRole) => {
                            actualUser?.roles.add(nonArrestRole)
                        }
                    )
                } else {
                    actualUser?.roles.add("756551568387473580")
                }

                delete inMemoryDB.users[targetUser.id].nonArrestRoles

                message.channel.send("Done!")
                return
            }

            message.channel.send(makeError("No such user found!"))
        }
    },
})

export default Pardon
