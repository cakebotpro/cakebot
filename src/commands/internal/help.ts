import Command from "../commands"
import createEmbed from "../../util/embeds"

const Help: Command = {
    name: "help",
    execute(args, message) {
        message.channel.send(
            createEmbed(
                "Help",
                "You can check out [this page of our website](https://cakebot.club/docs/commands/) for a full command list!"
            )
        )
    },
}

export default Help
