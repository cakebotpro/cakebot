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
import type { Guild, GuildMember, TextChannel, User } from "discord.js"
import { warn } from "../../../util/logging"
import Command from "../../commands"
import { addUserById, inMemoryDB } from "../../../data/database"
import { makeError } from "../../../util/constants"

function cancel(user: GuildMember, guild: Guild): void {
    if (!inMemoryDB.users[user.id]) {
        addUserById(user.id)
    }

    const channel = guild.channels.cache.get("783367524250157076") as
        | undefined
        | TextChannel

    channel?.send(
        `:police_car: :police_officer: <@!${user?.id}> **HAS BEEN ARRESTED**!`
    )

    const roleIds: string[] = []

    user?.roles.cache.each((value) => {
        roleIds.push(value.id)
        user.roles.remove(value).catch((e) => {
            warn(e)
        })
    })

    inMemoryDB.users[user.id].nonArrestRoles = roleIds

    user?.roles.add("768175383115202620")
}

const Arrest = (admins: readonly string[]): Command => ({
    name: "arrest",
    aliases: ["cancel"],
    execute(args, message) {
        const { guild } = message

        if (guild?.id === "702175596838649937") {
            const targetUser: User | undefined = message.mentions.users.first()

            if (!admins.includes(message.author.id)) {
                message.channel.send(makeError("You can't do that!!"))
                return
            }

            if (targetUser) {
                const actualUser = guild.member(targetUser)
                message.channel.send(
                    "Understood. Please allow a few seconds for cancellation to be executed."
                )
                if (actualUser !== null) {
                    cancel(actualUser, guild)
                }
                message.channel.send("Done!")
                return
            }

            message.channel.send(makeError("No such user/role found!"))
        }
    },
})

export default Arrest
