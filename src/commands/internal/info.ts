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
import createEmbed from "../../util/embeds"
import Command from "../commands"

const Info: Command = {
    name: "info",
    aliases: ["server-info"],
    execute(args, message) {
        message.channel.send(
            createEmbed("Server Info", `${message.guild?.name}'s Details`, [
                {
                    name: ":crown: Owner",
                    value: `${message.guild?.owner?.displayName}`,
                    inline: true,
                },
                {
                    name: ":grinning: Members",
                    value: `${message.guild?.memberCount}`,
                    inline: true,
                },
                {
                    name: ":map: Region",
                    value: `${message.guild?.region}`,
                    inline: true,
                },
                {
                    name: ":id: ID",
                    value: `${message.guild?.id}`,
                    inline: true,
                },
                {
                    name: ":comet: Nitro Booster Count",
                    value: `${message.guild?.premiumSubscriptionCount}`,
                    inline: true,
                },
                {
                    name: ":timer: Created At",
                    value: `${message.guild?.createdAt.toLocaleString()}`,
                    inline: true,
                },
                {
                    name: ":ballot_box_with_check: Is Verified",
                    value: `${message.guild?.verified}`,
                    inline: true,
                },
                {
                    name: ":abcd: Name Acronym",
                    value: `${message.guild?.nameAcronym}`,
                    inline: true,
                },
                {
                    name: ":purple_circle: Server Nitro Boost Perks Tier",
                    value: `${message.guild?.premiumTier}`,
                    inline: true,
                },
            ])
        )
    },
}

export default Info
