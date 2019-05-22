import discord


def prep(
    title,
    description
):
    # embed metadata
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x663399
    )
    # footer
    embed.set_footer(text="Created with ❤ and 🍪 by jumbocakeyumyum#0001")
    return embed


def build_help_menu(base):
    base.add_field("help", "Show this menu.")
    base.add_field("ping", "Check if bot is online.")
    return base
