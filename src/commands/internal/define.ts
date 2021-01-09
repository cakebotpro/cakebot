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
import { EmbedField } from "discord.js"
import define from "../../data/words"
import createEmbed from "../../util/embeds"
import Command from "../commands"

const Define: Command = {
    name: "define",
    aliases: ["meanings", "whatis"],
    execute(args, message) {
        if (args[0]) {
            define(args[0])
                .then((resp) => {
                    const embed = createEmbed(
                        `Define ${args[0]}`,
                        `Syllables: ${resp.syllables}`,
                        resp.defs.map(
                            (def) =>
                                ({
                                    name: "Definition",
                                    value: def,
                                    inline: false,
                                } as EmbedField)
                        )
                    )
                    message.channel.send(embed)
                    return
                })
                .catch(() => message.channel.send("Word not found!"))
        } else {
            message.channel.send("Please specify a word!")
        }
    },
}

export default Define
