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
import { addHook } from "pirates"

/**
 * Repairs a number of things that are very much broken.
 * Please, please, please DO NOT PATCH OVER THIS.
 * One layer of runtime patching will do, don't shoot us in the foot.
 * @private
 */
function patch(module: string): string {
    // common solutions
    const NOOP = `void 0;`

    // hack to create a clone of the string
    let m = `${module}`
    // fstream
    m = m.replace(`self.emit('error', err);`, NOOP)
    m = m.replace(`self.emit('error', er)`, NOOP)

    return m
}

addHook(
    function runtimePatching(code) {
        return patch(code)
    },
    {
        exts: [".js"],
        matcher: (f) => f.includes("fstream"),
        ignoreNodeModules: false,
    }
)
