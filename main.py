import discord
import area4

Bot_Prefix = "+"

client = discord.ext.commands.Bot(command_prefix = Bot_Prefix)

@client.event
async def on_ready():
    """
    Called when the bot is booted

    :return: nothing
    :rtype: None
    """
    await client.change_presence(game=discord.Game(name="Being beta tested"))

    print(area4.divider(1))
    print("Ready to role, I'll see you on Discord: @", client.user)
    print(area4.divider(1))

@client.event
async def on_message(message):
    """
    Called on message

    :return: nothing
    :rtype: None
    :param message: the message object
    """
    if message.author == client.user:
        # cancel own messages
        return
    else:
    if not message.content.startswith(Bot_Prefix):
        # normal message
	      return
    # asking for bot
    theinput = message.content[len(prefix):]
    args = theinput.split()
    # the command, e.x. "help"
    cmd = args[0].lower()
    # the args (array) e.x. ["hello", "world"]
    args = args[1:]
