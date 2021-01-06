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
