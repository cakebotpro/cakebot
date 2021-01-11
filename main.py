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
async def on_ready():
    await client.change_presence(
        activity=discord.Game(name=base_conf["status"])
    )
    secho(
        "\nReady to roll, I'll see you on Discord: @" + str(client.user),
        fg="green",
    )


@client.event
async def on_message(message):
    BOT_PREFIX = "+"

    if getenv("PRODUCTION") is None:
        BOT_PREFIX = "-"

    if not message.content.startswith(BOT_PREFIX):
        return

    # Split input
    args = message.content[len(BOT_PREFIX) :].split()

    if len(args) == 0:
        return

    cmd = args[0].lower()

    # the arg array ex. ["hello", "world"]
    args = args[1:]

    await PyramidServer.on_command(cmd, args, message)

    s = message.channel.send

    if message.author.id in UserUtil.banned_users():
        return await s(
            " ".join(
                [
                    "**You have been banned from using the bot.**",
                    "This typically happens because you abused a feature, or caused a major problem for our team.",
                    "You may not appeal this.",
                ]
            )
        )

    elif cmd == "invite":
        return await s(
            embed=EmbedUtil.prep(
                "Invite Cakebot",
                f"[Click here to invite me!]({oauth_url(580573141898887199, permissions=required_permissions)})",
            )
        )

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

    elif cmd == "cookie" or cmd == "cookies":
        subcommand = args[0]
        args = args[1:]
        userId = TextCommandsUtil.get_mentioned_id(args)

        if subcommand in ["balance", "bal"]:
            count = 0
            if userId == 0:
                # assume user wants themself
                count = Database.get_count(message.author.id, config)
            else:
                count = Database.get_count(userId, config)

            return await s(
                embed=EmbedUtil.prep(
                    title="Cookies",
                    description=f"User has {count} cookies.",
                )
            )

        elif subcommand in ["give", "to"]:
            if userId == 0:
                return await s(
                    "I don't see who I should give the cookie to. Try mentioning them."
                )

            new_count = Database.add_cookie(userId, config)

            return await s(
                f"Gave <@!{userId}> a cookie. They now have {new_count} cookies."
            )