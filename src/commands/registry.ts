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

            if ((obj as any)[property] === value) {
                returnValue = obj
            }
        })

        return returnValue
    }
}
