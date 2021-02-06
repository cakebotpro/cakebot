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

// 16 bit integer limit
export const REMOVAL_MARKER = 32_766

/**
 * Remove an object from the array if a condition is met.
 */
export function removeIf<T>(array: T[], cond: (item: T) => boolean): T[] {
    array.forEach((value, index) => {
        if (cond.call(array, value)) {
            // @ts-ignore
            array[index] = REMOVAL_MARKER
        }
    })

    // @ts-ignore
    return array.filter((value) => value !== REMOVAL_MARKER, array)
}
