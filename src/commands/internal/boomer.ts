import Command from "../commands"
import { MessageAttachment } from "discord.js"

const Boomer: Command = {
    name: "boomer",
    execute(args, message) {
        const picture = new MessageAttachment(
            "https://raw.githubusercontent.com/cakebotpro/cakebot/master/content/boomer.jpeg"
        )
        message.channel.send(picture)
    },
}

export default Boomer
