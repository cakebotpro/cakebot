/**
 * Cakebot - A fun and helpful Discord bot
 * Copyright (C) 2021-current year  Reece Dunham
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { Guild, VoiceChannel } from "discord.js"
import Command from "../../commands"

function muteAll(guild: Guild): void {
    // eslint-disable-next-line
    const channel = guild.channels.cache.get("765693920126304256") as
        | undefined
        | VoiceChannel

    channel?.members.each((member) => {
        member.edit({ mute: true })
    })
}

const MuteAll = (admins: readonly string[]): Command => ({
    name: "muteall",
    aliases: ["sm"],
    execute(args, message) {
        const { guild } = message

        if (guild?.id === "702175596838649937") {
            if (!admins.includes(message.author.id)) {
                message.channel.send("You can't do that!!")
                return
            }

            muteAll(guild)
        }
    },
})

export default MuteAll
