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

import logging from "../util/logging"
import Command from "./commands"

/**
 * A 'registry' allows for easy indexing and registering of items of a certain type.
 */
export default class Registry {
    /**
     * The objects this registry holds.
     */
    private objects: Command[]

    public constructor() {
        this.objects = []
    }

    /**
     * Registers the passed object to this registry.
     *
     * @param obj The object to register.
     * @returns Nothing.
     */
    public register(obj: Command): void {
        this.objects.push(obj)
        logging.debug(`Registered command ${obj.name}.`)
    }

    /**
     * Registers all the objects in the passed array to this registry.
     *
     * @param obj The array of objects to register.
     * @returns Nothing.
     */
    public registerAll(obj: Command[]): void {
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
     * @returns The entry you requested, or null.
     */
    public find<V>(property: string, value: V): Command | null {
        let returnValue: Command | null = null

        this.objects.forEach(function registryFindIterator(obj) {
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
