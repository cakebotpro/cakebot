import Command from "../commands"
import * as Database from "../../data/database"
import { makeError } from "../../util/constants"

const Prefix: Command = {
    name: "prefix",
    aliases: ["setprefix"],
    async execute(args, message) {
        if (!message.guild) {
            message.channel.send(
                makeError(
                    "You are in direct messages, not a server! You can't use this here."
                )
            )
            return
        }

        if (args.length < 1) {
            message.channel.send(
                `This server's prefix is '${
                    Database.inMemoryDB.servers[message.guild?.id ?? ""].prefix
                }'`
            )
            return
        }

        /*
        try {
            // @ts-ignore
            if (hasP("MANAGE_GUILD")) {
                message.channel.send(
                    makeError(
                        "You don't have manage server or administrator permissions, so you can't do that!"
                    )
                )
                return
            }
        } catch (e) {
            console.trace(e.stack)
        }

        if (args.length === 1) {
            Database.inMemoryDB.servers[message.guild?.id ?? ""].prefix =
                args[1]
            console.log("here 2")
            message.channel.send(
                `Okay, I've set this server's prefix to '${args[1]}'. You can now run commands by typing something like '${args[1]}help'`
            )
        }
         */
    },
}

export default Prefix
