import { MessageEmbed, EmbedField } from "discord.js"

export default function createEmbed(
    title: string,
    description: string,
    fields?: EmbedField[]
): MessageEmbed {
    const e = new MessageEmbed()

    e.setTitle(title)
    e.setDescription(description)
    e.setAuthor(
        "Cakebot",
        "https://raw.githubusercontent.com/cakebotpro/cakebot/master/content/cake.png",
        "https://cakebot.club"
    )
    e.setFooter(
        "Created with ❤ and 🍪 by the Cakebot Team | https://cakebot.club"
    )

    if (fields !== void 0) {
        e.addFields(...fields)
    }

    return e
}
