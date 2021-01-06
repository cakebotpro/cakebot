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
import registry from "../commands/registry"

describe("registry operations", () => {
    it("can create a basic registry", () => {
        const r = new registry()

        r.register("hi")
        r.register("hello")

        expect(r.objects).toEqual(["hi", "hello"])
    })

    it("registerAll works", () => {
        const r = new registry()

        r.register("test")
        r.registerAll(["heya", "fggdgd"])

        expect(r.objects).toEqual(["test", "heya", "fggdgd"])
    })

    it("find works", () => {
        const r = new registry()

        r.register({ name: "coolthings" })
        r.register({ name: "otherthings", data: "jighdifg" })
        r.register({ name: "finalthings" })

        expect(r.find("name", "otherthings")).toStrictEqual({
            name: "otherthings",
            data: "jighdifg",
        })
    })
})
