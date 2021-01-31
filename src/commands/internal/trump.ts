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
import { asyncGetAndConsume } from "../../data/remote/runtime-downloads"
import createEmbed from "../../util/embeds"

interface RandomQuoteResponse {
    appeared_at: string
    value: string
}

const Trump: Command = {
    name: "trump",
    aliases: ["donaldtrump", "don", "trumpquote", "donquote"],
    execute(args, message) {
        asyncGetAndConsume(
            "https://tronalddump.io/random/quote",
            (response) => {
                const r: RandomQuoteResponse = (response as unknown) as RandomQuoteResponse

                message.channel.send(
                    createEmbed(
                        "Donald Trump Quote",
                        `"**${r.value}**" - Donald J. Trump, ${new Date(
                            r.appeared_at
                        ).toLocaleDateString()}`
                    )
                )
            }
        )
    },
}

export default Trump
