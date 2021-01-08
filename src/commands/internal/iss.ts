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
// @ts-ignore
import decoder from "google-geo-decoder"
import { getConfig } from "../../data/config"
import { asyncGetAndConsume } from "../../data/remote/runtime-downloads"
import Command from "../commands"

interface ExpectedResponseData {
    iss_position: {
        latitude: string
        longitude: string
    }
}

const Iss: Command = {
    name: "iss",
    execute(args, message) {
        asyncGetAndConsume(
            "http://api.open-notify.org/iss-now.json",
            (response) => {
                const data = ((response as unknown) as ExpectedResponseData)
                    .iss_position
                const key = getConfig().googleMapsApiKey
                if (!key) {
                    message.channel.send(
                        "Error: this module is improperly configured. You need a Google Maps API key!"
                    )
                }
                console.log(decoder(data.latitude, data.longitude, key))
            }
        )
    },
}

export default Iss
