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
 * Logs a message at the 'info' level.
 * @param message The message.
 */
export function info(message: string): void {
    console.log(chalk`{blue info} ${message}`)
}

/**
 * Logs a message at the 'warning' level.
 * @param message The message.
 */
export function warn(message: string): void {
    console.log(chalk`{yellow warn} ${message}`)
}

/**
 * Logs a message at the 'error' level.
 * @param message The message.
 */
export function error(message: string): void {
    console.log(chalk`{red error} ${message}`)
}

/**
 * Logs a message at the 'debug' level, which requires `env.DEBUG` to be `"true"`.
 * @param message The message.
 * @param force If it should ignore the debug option and print anyway.
 * @see https://cakebot.club/docs/selfhosting/environment-variables
 */
export function debug(message: string, force?: boolean): void {
    let r

    if (force === true) {
        r = true
    } else {
        r = getConfig().debug
    }

    if (r === true) {
        console.log(chalk`{magenta debug} ${message}`)
    }
}
