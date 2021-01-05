import Command from "../commands"

const Ping: Command = {
    name: "ping",
    aliases: ["pong", "hello"],
    execute(args, message) {
        message.channel.send("Pong! I'm online I think?")
    },
}

export default Ping
