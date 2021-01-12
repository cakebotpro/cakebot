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
import { createTicket } from "../../data/database"
import Command from "../commands"

const Report: Command = {
    name: "report",
    aliases: ["ticket"],
    execute(args, message) {
        if (args.length >= 2) {
            createTicket({ author: message.author, message: args.join(" ") })
                .then(() => {
                    message.channel.send(
                        "Ticket opened! Please wait for a team member to review it."
                    )
                    return
                })
                .catch((err) => {
                    message.channel.send(`Error!: ${err}`)
                })
        } else {
            message.channel.send("Your message is too short!")
        }
    },
}

export default Report
