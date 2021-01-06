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

/**
 * Either the type parameter or null.
 * This gets reused multiple times so its just easier to have a global type for it.
 */
type VirtualOptional<T> = T | null

/**
 * A 'registry' allows for easy indexing and registering of items of a certain type.
 */
export default class Registry<T> {
    /**
     * The objects this registry holds. DO NOT modify outside this class!!
     */
    objects: T[]

    constructor() {
        this.objects = []
    }

    /**
     * Registers the passed object to this registry.
     *
     * @param obj The object to register.
     */
    register(obj: T): void {
        this.objects.push(obj)
    }

    /**
     * Registers all the objects in the passed array to this registry.
     *
     * @param obj The array of objects to register.
     */
    registerAll(obj: T[]): void {
        obj.forEach((o) => this.objects.push(o))
    }

    /**
     * Finds the first object in the object set that has the property with the specified value.
     * E.g. if you do find("name", "hello") it finds the first object with the name property set
     * to hello.
     * It's a complex implementation because we also have to account for TypeScript, and if the
     * value of the property is an array we also search inside the array for the value we want.
     *
     * @param property The name of the property to check.
     * @param value The value to check for.
     */
    find<V>(property: string, value: V): VirtualOptional<T> {
        let returnValue: VirtualOptional<T> = null

        this.objects.forEach((obj) => {
            if (returnValue !== null) {
                return
            }

            if (Array.isArray((obj as never)[property])) {
                if (((obj as never)[property] as Array<V>).includes(value)) {
                    returnValue = obj
                }
            }

            if ((obj as never)[property] === value) {
                returnValue = obj
            }
        })

        return returnValue
    }
}
