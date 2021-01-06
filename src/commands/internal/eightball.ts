import Command from "../commands"
import { eightballs } from "../../data/runtime-data"
import random from "random"

const EightBall: Command = {
    name: "8ball",
    aliases: ["8", "eightball", "eight"],
    execute(args, message) {
        message.channel.send(eightballs[random.int(0, eightballs.length - 2)])
    },
}

export default EightBall
