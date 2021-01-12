"""
Cakebot - A fun and helpful Discord bot
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

@client.event
async def on_message(message):

    elif cmd == "info":
        return await s(
            embed=EmbedUtil.prep(
                "Server Info",
                TextCommandsUtil.make_server_info(
                    message.guild.name,
                    str(message.guild.owner),
                    len(message.guild.members),
                    message.guild.region,
                    message.guild.id,
                    message.guild.premium_subscription_count,
                    str(message.guild.is_icon_animated()),
                    str(message.guild.created_at),
                    str(message.guild.large),
                    str(message.guild.mfa_level == 1),
                    str(message.guild.premium_tier),
                ),
            )
        )

    elif cmd == "report":
        return await GitHubUtil.report(s, g, args, message)

    elif cmd == "iss":
        m = await s("Calculating...")
        imp = IssApi.IssLocater()
        lat = imp.lat
        lon = imp.lon
        from reverse_geocoder import search

        geodata = search((lat, lon))
        location = "{0}, {1}".format(geodata[0]["admin1"], geodata[0]["cc"])

        await m.delete()
        return await s(
            embed=EmbedUtil.prep(
                "International Space Station", "Where it is right now!"
            )
            .add_field(
                name="Location above Earth", value=str(location), inline=False
            )
            .add_field(name="Latitude", value=str(lat), inline=False)
            .add_field(name="Longitude", value=str(lon), inline=False)
        )

    elif cmd == "reboot":
        if message.author.id in UserUtil.admins():
            await s("Restarting. This may take up to 5 minutes.")
            # make the bot crash, forcing our server to turn it back on
            _exit(1)
        else:
            return await s(":x: **You are not authorized to run this!**")
