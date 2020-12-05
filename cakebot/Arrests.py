"""
Cakebot - A cake themed Discord bot
Copyright (C) 2019-current year  Reece Dunham

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from cakebot import TextCommandsUtil
from discord import Guild, Member, User, Role, VoiceChannel, utils

from typing import List


async def on_command(command, args, message):
    if not message.channel.guild.id == 702175596838649937:
        return

    if command == "arrest":
        person = TextCommandsUtil.get_mentioned_id(args)
        has_admin = False
        for role in message.author.roles:
            if role.id in [719341716154482830, 780522489272729661]:
                has_admin = True

        if has_admin:
            guild: Guild = message.channel.guild
            await guild.get_channel(783367524250157076).send(
                ":police_car: :police_officer: <@!"
                + str(person)
                + "> **HAS BEEN ARRESTED**!"
            )
            member: User = guild.get_member(person)
            await message.channel.send(
                "Understood. Please allow a few seconds for cancellation to be processed."
            )
            for role in await guild.fetch_roles():
                try:
                    await member.remove_roles(role, reason="ARRESTED!")
                except:
                    print("Skipping role")
            cancelled_roles: List[Role] = [
                utils.get(await guild.fetch_roles(), id=768175383115202620)
            ]
            await member.add_roles(*cancelled_roles, reason="ARRESTED!")
        else:
            return await message.channel.send("bruh you can't do that")

    elif command == "pardon":
        return await message.channel.send("bruh thats not implemented yet")

    elif command == "sm":
        has_admin = False
        for role in message.author.roles:
            if role.id in [719341716154482830, 780522489272729661]:
                has_admin = True

        if has_admin:
            vc: VoiceChannel = message.channel.guild.get_channel(765693920126304256)
            members: List[Member] = vc.members
            has_muted = False
            for member in members:
                if member.voice.mute and not has_muted:
                    has_muted = True
                member.voice.mute = not has_muted
                member.voice.deaf = not has_muted
                await member.edit(mute=(not has_muted), deafen=(not has_muted))
            return await message.channel.send("Done!")
        else:
            return await message.channel.send("bruh you can't do that")
