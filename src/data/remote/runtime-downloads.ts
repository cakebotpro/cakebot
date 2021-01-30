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
import fetchPromise, { RequestInit } from "node-fetch"

export type AsyncConsumer = (
    data: Record<string, string | number | never>
) => void

/**
 * Downloads the file content, and calls the callback with the value of the JSON data.
 * @param url The URL to fetch the JSON content of.
 * @param callback The callback for the data that accepts the fetched JSON.
 * @param options The fetch options.
 * @returns Nothing, this uses a callback!
 */
export const asyncGetAndConsume = (
    url: string,
    callback: AsyncConsumer,
    options?: RequestInit
): void => {
    fetchPromise(url, options || {})
        .then((response) => response.json())
        .then((jsondata) => {
            // eslint-disable-next-line promise/no-callback-in-promise
            callback(jsondata)
            return
        })
        .catch((e) => {
            throw e
        })
}
