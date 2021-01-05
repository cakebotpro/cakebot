import commander from "commander"
import start from "."
import { config as configureEnvironment } from "dotenv"

configureEnvironment()

commander.name("Cakebot")

commander.command("run").description("Run the bot.").action(start)

commander.parse(process.argv)
