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
import { init, lookUp, StringPoint } from "../../data/remote/geocoder"
import { asyncGetAndConsume } from "../../data/remote/runtime-downloads"
import createEmbed from "../../util/embeds"
import Command from "../commands"
import { makeError } from "../../util/constants"

init()

interface OpenNotifyResponseData {
    iss_position: StringPoint
}

const Iss: Command = {
    name: "iss",
    execute(args, message) {
        asyncGetAndConsume(
            "http://api.open-notify.org/iss-now.json",
            (response) => {
                const data = ((response as unknown) as OpenNotifyResponseData)
                    .iss_position

                const coords: StringPoint = {
                    latitude: data.latitude,
                    longitude: data.longitude,
                }

                const result = lookUp(coords)
                if (result === null) {
                    message.channel.send(
                        makeError(
                            "Something went wrong, we will investigate. Sorry!"
                        )
                    )
                    return
                }

                message.channel.send(
                    createEmbed(
                        "ISS",
                        "The current location of the international space station!",
                        [
                            {
                                name: "Latitude",
                                value: data.latitude,
                                inline: true,
                            },
                            {
                                name: "Longitude",
                                value: data.longitude,
                                inline: true,
                            },
                            {
                                name: "Relative location (closest city)",
                                value: `${result.name}, ${result.countryCode}`,
                                inline: true,
                            },
                        ]
                    )
                )
            }
        )
    },
}

export default Iss
