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

type VirtualOptional<T> = T | null

export default class Registry<T> {
    objects: T[]

    constructor() {
        this.objects = []
    }

    register(obj: T): void {
        this.objects.push(obj)
    }

    registerAll(obj: T[]): void {
        obj.forEach((o) => this.objects.push(o))
    }

    find<V>(property: string, value: V): VirtualOptional<T> {
        let returnValue: VirtualOptional<T> = null

        this.objects.forEach((obj) => {
            if (returnValue !== null) {
                return
            }

            if (Array.isArray((obj as any)[property])) {
                if (((obj as any)[property] as Array<V>).includes(value)) {
                    returnValue = obj
                }
            }

            if ((obj as any)[property] === value) {
                returnValue = obj
            }
        })

        return returnValue
    }
}
