import Command from "../commands"
import { jokes } from "../../data/runtime-data"
import random from "random"

const Joke: Command = {
    name: "joke",
    aliases: ["getjoke"],
    execute(args, message) {
        message.channel.send(jokes[random.int(0, jokes.length - 1)])
    },
}

export default Joke
