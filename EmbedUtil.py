import discord

def classic(
    title,
    description,
    sectionNames,
    sectionContents
):
    """
    Create a simple embed
    :Note: make sure that sectionNames and sectionContents
           are aligned

    :Example:
    sectionNames[1]
    # must go with
    sectionContents[1]

    :param title: the title of the embed (string)
    :param description: the embed description (string)
    :param sectionNames: array of section names
    :param sectionContents: array of section contents
    :return: generated embed
    :rtype: discord.Embed
    """
    # embed metadata
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x663399
    )
    # footer
    embed.set_footer(text="Created with ❤ and 🍪 by jumbocakeyumyum#0001")
    # dynamic content
    for i,x in enumerate(sectionNames):
        embed.add_field(
            name=sectionNames[i],
            value=sectionContents[i]
        )
        if x > 1000: # just to get flake8 to shut up
            return
    return embed
