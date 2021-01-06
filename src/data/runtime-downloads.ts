/**
 * I don't want to have to go through the hassle of manually packaging files, so we just download them at runtime.
 * This also allows them to be updated without needing a new release.
 */

// @ts-ignore
import fetch from "sync-fetch"
import logger from "../util/logging"

const getFileContents = (url: string): string[] => {
    logger.debug(`Downloading external component: ${url}`)

    return fetch(url).text().split("\n")
}

export default getFileContents
