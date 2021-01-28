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
import random from "random"
import { eightballs } from "../../data/remote/runtime-data"
import Command from "../commands"
import { makeError } from "../../util/constants"

const EightBall: Command = {
    name: "8ball",
    aliases: ["8", "eightball", "eight"],
    execute(args, message) {
        if (args.length < 1) {
            message.channel.send(
                makeError(
                    "I can't answer your question... you didn't give me one!"
                )
            )
            return
        }

        message.channel.send(eightballs[random.int(0, eightballs.length - 2)])
    },
}

export default EightBall
