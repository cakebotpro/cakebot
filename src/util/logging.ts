import chalk from "chalk"
import { getConfig } from "../data/config"

export default {
    info: (message: string): void => {
        console.log(chalk`{blue info} ${message}`)
    },
    warn: (message: string): void => {
        console.log(chalk`{yellow warn} ${message}`)
    },
    error: (message: string): void => {
        console.log(chalk`{red error} ${message}`)
    },
    debug: (message: string): void => {
        if (getConfig().debug) {
            console.log(chalk`{magenta debug} ${message}`)
        }
    },
}
