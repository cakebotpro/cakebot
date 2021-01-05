import chalk from "chalk"

/**
 * Used to give our errors actual context, so we can
 * contact the person who caused it for more details if need be.
 */
export class Trace {
    command: string
    args: string[]
    user: string

    constructor(command: string, args: string[], user: string) {
        this.command = command
        this.args = args
        this.user = user
    }

    toString(): string {
        return chalk`[{blue User:} ${this.user}] [{blue Command:} ${
            this.command
        }] [{blue Arguments}]: ${this.args.join(" ")}`
    }
}
