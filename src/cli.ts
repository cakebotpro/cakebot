import commander from "commander"
import { config as configureEnvironment } from "dotenv"
import { banner } from "./util/constants"

configureEnvironment()

console.log(banner)

// prepopulate data
import "./data/runtime-data"
import start from "."

commander.name("Cakebot")

commander.command("run").description("Run the bot.").action(start)

commander.parse(process.argv)
