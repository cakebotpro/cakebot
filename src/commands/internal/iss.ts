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
import geocoder from "../../data/remote/geocoder"
import { asyncGetAndConsume } from "../../data/remote/runtime-downloads"
import createEmbed from "../../util/embeds"
import logging from "../../util/logging"
import Command from "../commands"

// @ts-ignore
geocoder.init({})

interface ExpectedResponseData {
    iss_position: {
        latitude: string
        longitude: string
    }
}

// the found... city object... ish
// todo this should get a better name
interface Find {
    countryCode: string
    name: string
}

const Iss: Command = {
    name: "iss",
    execute(args, message) {
        asyncGetAndConsume(
            "http://api.open-notify.org/iss-now.json",
            (response) => {
                const data = ((response as unknown) as ExpectedResponseData)
                    .iss_position

                const coords = {
                    latitude: data.latitude,
                    longitude: data.longitude,
                }

                // @ts-ignore
                geocoder.lookUp(
                    [coords],
                    function cbCallback(err?: string, res?: never) {
                        if (err) {
                            logging.error(err)
                        }

                        // @ts-ignore
                        const f: Find = res[0][0]

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
                                        name:
                                            "Relative location (closest city)",
                                        value: `${f.name}, ${f.countryCode}`,
                                        inline: true,
                                    },
                                ]
                            )
                        )
                    }
                )
            }
        )
    },
}

export default Iss
