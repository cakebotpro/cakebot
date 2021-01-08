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
// @ts-ignore
import fetch from "sync-fetch"
import logger from "../../util/logging"

/**
 * I don't want to have to go through the hassle of manually packaging files, so we just download them at runtime.
 * This also allows them to be updated without needing a new release.
 *
 * @param url The remote file's url.
 */
const getFileContents = (url: string): string[] => {
    logger.debug(`Downloading external component: ${url}`)

    return fetch(url).text().split("\n")
}

type AsyncConsumer = (data: Record<string, string | number | never>) => void

/**
 * Downloads the file content, and calls the consumer with the value of the JSON data.
 *
 * @param url The URL to fetch the JSON content of.
 * @param consumer The consumer of the data that accepts the fetched JSON data.
 * @param options The fetch options.
 */
export const asyncGetAndConsume = (
    url: string,
    consumer: AsyncConsumer,
    options?: RequestInit
): void => {
    fetchPromise(url, options || {})
        .then((response) => response.json())
        .then((jsondata) => {
            consumer(jsondata)
            return
        })
        .catch((e) => {
            throw e
        })
}

export default getFileContents
