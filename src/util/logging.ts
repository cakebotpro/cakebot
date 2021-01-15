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
import chalk from "chalk"
import { getConfig } from "../data/config"

/**
 * A very basic logger.
 *
 * @example
 * logging.info("Hello world") // in console => info Hello world
 */
export default {
    info: (message: string): void => {
        console.log(chalk`{blue info} ${message}`)
    },
    warn: (message: string): void => {
        console.log(chalk`{yellow warn} ${message}`)
    },
    error: (message: string): void => {
        console.log(chalk`{red error} ${message}`)
    },
    debug: (message: string): void => {
        if (getConfig().debug) {
            console.log(chalk`{magenta debug} ${message}`)
        }
    },
}
