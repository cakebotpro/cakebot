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
import geocoder from "local-reverse-geocoder"
import { asyncGetAndConsume } from "../../data/remote/runtime-downloads"
import logging from "../../util/logging"
import Command from "../commands"

geocoder.init({
    load: {
        admin1: false,
        admin2: false,
        admin3And4: false,
        alternateNames: false,
    },
})

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

                const coords = {
                    latitude: data.latitude,
                    longitude: data.longitude,
                }

                geocoder.lookUp(
                    coords,
                    function cbCallback(err?: string, res?: never) {
                        if (err) {
                            logging.error(err)
                        }

                        logging.info(JSON.stringify(res, null, 2))
                    }
                )
            }
        )
    },
}

export default Iss
