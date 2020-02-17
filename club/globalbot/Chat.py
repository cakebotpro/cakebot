import io  # Needed for bytes input-output (io.bytesIO)
import re  # Needed for regex searching
import typing  # Needed for more complex type hints
import asyncio  # Needed for gathering all the send message promises
import aiohttp  # Needed for making a webhook (as an adapter)
import discord  # Needed for practically everything discord-ey
from discord.ext import commands  # Needed for creating a cog

from utils import checks, save, filter
# Checks is used for our custom checks, for example our bypass check
# Save is a custom class to save our JSON data. This will soon be replaced by sqlalchemy
# Filter is a custom class to filter out images that aren't valid images
from utils.classes import Author


# Author is a custom class allowing us to get emojis for different authors etc.
# (It's not just done in our send method as we need it for feeds too...)


class Chat(commands.Cog, name="chat"):
    def __init__(self, bot):
        self.bot = bot  # Set our bot so that we can use it in other functions
        self.config = save.Save("chat/links")  # Get a save instance for links so that we can link our chat channels
        self.bans = save.Save("all/bans")  # Get our global bans so that we can stop users from using the chat
        self.filter = filter.Filter()  # Create a filter for stopping attachments before they cause trouble

    async def send(self, ctx, channels: typing.Union[typing.List[str], bool], user, message: str,
                   bypass: bool = False, text_to_speech: bool = False,
                   files: typing.List[discord.Attachment] = ()):
        try:
            await ctx.message.add_reaction("⏱️")  # Add a reaction to let the user know something is happening
        except discord.HTTPException:  # If we can't add the reaction
            pass  # Ignore the error
        log_embed = discord.Embed(title=f"{user.emote} ({user._emote}) > {user.author.name} ({user.author.id})"[-80:],
                                  description=message)  # Create an embed that will be used to log our message
        log_embed.set_thumbnail(url=user.author.avatar_url)  # Let us see their avatar
        # Show us some basic info about the message
        log_embed.add_field(name="Using TTS", value="Yes" if text_to_speech else "No", inline=False)
        log_embed.add_field(name="Using Anonymous Mode", value="Yes" if user.author.id != user.id else "No",
                            inline=False)
        log_embed.add_field(name="Unfiltered", value="Yes" if bypass else "No",
                            inline=False)
        log_embed.add_field(name="From guild", value=f"{ctx.guild} ({ctx.guild.id})", inline=False)
        log_embed.add_field(name="To channels", value=f"{'all channels' if channels is True else ', '.join(channels)}",
                            inline=False)
        # There's our basic info ^. It should be fairly self explanatory
        read_files = [(file, await file.read()) for file in files]
        # Create a list of files that been read, so we don't have to read them repeatedly
        clean_files = []  # Create a list of files that have been cleaned by our filter: these ones will get sent
        unclean_files = []  # Create a list of files that have not been cleaned: these ones will be logged
        content = message  # Create a copy of our message which we will mutate, we will later check if these are equal
        if not bypass:  # If we're not in bypass mode:
            for file in read_files:  # For every file
                cleaned_file = await self.filter.clean(*file)  # Clean the file using our filter
                if cleaned_file:  # If the file has not been totally removed
                    clean_files.append(cleaned_file)  # Add our clean file to the list of cleaned files
            for domain in self.bot.domains:  # For every valid domain extension in our domains
                content = re.sub(
                    r"(https?:\/\/)?([a-z0-9]+ ?(\.|dot) ?)+(" + domain + ")\/?([\w]*\/*)*(#[^?\s]*)?(\?\S*)?", "",
                    content, flags=re.MULTILINE
                )  # Replace any urls with whitespace to remove them
            # Pycharm claims \/\/ is useless escaping. Trust me, it's not useless
            content = await commands.clean_content(use_nicknames=False).convert(
                ctx,
                content
            )  # Clean mentions from our message, don't use nicknames so that the names are generalised across servers
        else:  # Or if we aren't being filtered
            for file in read_files:  # For every file
                clean_files.append({"read": file[1],
                                    "filename": file[0].filename,
                                    "spoiler": file[0].is_spoiler()})  # Add the file to our list of cleaned files
                # without questioning it
        for file in read_files:  # For every file
            unclean_files.append({"read": file[1],
                                  "filename": file[0].filename,
                                  "spoiler": file[0].is_spoiler()})  # Add the file to our list of unclean files

        content = content.strip()  # Remove whitespace at the start and end of the content (useful if the message ended
        # with a url, for example)
        content = content[:2000]  # Remove every character of content that's longer than 2000 characters from the end
        # The content could be longer than 2000 as mentions can be shorter than actual usernames
        if not content and len(clean_files) < 1:  # If content is empty and no files have been let through the filter
            try:
                log_embed.colour = 0xaa0000  # Set the embed to red
                await self.bot.get_channel(645599322490011659).send(embed=log_embed, files=list(
                               discord.File(io.BytesIO(file["read"]), file["filename"], spoiler=file["spoiler"])
                               for file in unclean_files
                           ))  # Send the previous message to the logs
                await ctx.message.add_reaction("❌")  # Add the x reaction to the message to show we couldn't send it
            except discord.HTTPException:
                pass  # Ignore any errors
            return False  # Return False to show we couldn't send it
        try:
            if content != message or len(files) != len(clean_files):  # If we got filtered even a little bit
                log_embed.colour = 0xffd700  # Set the color to yellow/gold to show it was filtered
            else:
                log_embed.colour = 0x00aa00  # Set the color to green to show an unfiltered message
            await self.bot.get_channel(645599322490011659).send(embed=log_embed, files=list(
                               discord.File(io.BytesIO(file["read"]), file["filename"], spoiler=file["spoiler"])
                               for file in unclean_files
                           ))  # Send the log embed
            await ctx.message.add_reaction("💬")  # Add the 'sending' emoji so they know we're sending it
        except discord.HTTPException:
            pass  # Ignore any errors
        chats = []  # Create a list of all of our hooks
        chat_channels = self.config.load_data()  # Load our configuration data
        for chat in chat_channels:  # For every chat in the config
            if channels is True:  # If we're sending to every channel
                # SALL
                chats.append(chat_channels[chat]["hook"])  # Add the webhook to the list
            elif chat_channels[chat]["channel"] in channels:  # If the channels we are sending to would send to the hook
                chats.append(chat_channels[chat]["hook"])  # Add the webhook to the list
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                *[
                    discord.Webhook.from_url(
                        hook_url,
                        adapter=discord.AsyncWebhookAdapter(session)
                    ).send(content=content,
                           username=f"{user.emote} > {user} ({user.id})"[-80:],
                           avatar_url=user.avatar_url,
                           tts=text_to_speech,
                           files=list(
                               discord.File(io.BytesIO(file["read"]), file["filename"], spoiler=file["spoiler"])
                               for file in clean_files
                           ))
                    for hook_url in chats
                ], return_exceptions=True
            )  # Get all the coroutines for sending, and then send them
        try:
            await ctx.message.add_reaction("✔️")  # Add the 'sent' reaction to the message
        except discord.HTTPException:
            pass  # Ignore any errors
        return True  # Return True to let the calling function know it got sent

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message: discord.Message):
        chat_id = message.channel.id
        chat_channel = self.config.read_key(chat_id)
        banned = self.bans.read_key(message.author.id)
        ctx = await self.bot.get_context(message)
        author = Author(ctx)
        if message.content.startswith("=> "):
            return
        try:
            chat_channel["channel"]  # It does something, I swear
            chat_channel["hook"]  # It does something, I swear
        except (TypeError, KeyError):
            return
        if banned:
            if not banned.startswith("-silent"):
                await ctx.send(f"=> It looks like you're banned from the global chat\n> Reason: {banned}",
                               delete_after=5)
                return await message.delete()
            else:
                return await message.delete()
        if message.webhook_id:
            return await message.delete()
        elif message.author.bot or ctx.valid:
            return await message.delete()
        if message.content or message.attachments:
            if not await self.send(ctx, [chat_channel["channel"]], author, message.content, files=message.attachments):
                await ctx.send(
                    f"=> It seems that I couldn't send that message... did it have any content. Some things to "
                    f"note:\n"
                    f"- Links are automatically ignored\n"
                    f"- Embeds in messages are ignored",
                    delete_after=5)
        await message.delete()

    @commands.command(name='link', aliases=['🔗', 'connect'])
    @checks.bypass_check(checks.has_permissions_predicate, manage_messages=True, manage_webhooks=True)
    @commands.guild_only()
    async def link_chat(self, ctx, chat: str, channels: commands.Greedy[discord.TextChannel]):
        """Connect your chats together.

Run:
- %%link {{chat to link to (required)}} {{#mention as many channels as you want (optional)} """
        channels = [ctx.channel] if len(channels) < 1 else channels
        chat = discord.utils.escape_mentions(chat).replace("`", "'").replace("~", "-").strip()
        linked = 0
        for channel in channels:
            linked_channel = self.config.read_key(channel.id)
            if linked_channel:
                await ctx.send(f"The {channel.mention} channel is already linked to a chat (the "
                               f"`{linked_channel['channel']}` chat). Did you mean to "
                               f"{ctx.prefix}unlink first?")
            else:
                try:
                    hook = await channel.create_webhook(name=chat, reason=f"Linking channel to {chat}")
                    self.config.save_key(channel.id, {
                        "channel": chat,
                        "hook": hook.url
                    })
                    linked += 1
                    await ctx.send(f"Linked the {channel.mention} channel to `{chat}`")
                except discord.Forbidden:
                    await ctx.send(f"It looks like I don't have permissions to create webhooks in {channel.mention}, "
                                   f"give me the manage webhooks permission and try again")
        s = "" if linked == 1 else "s"
        await ctx.send(f"Linked {linked} channel{s}")

    @commands.command(name='unlink', aliases=['disconnect'])
    @checks.bypass_check(checks.has_permissions_predicate, manage_messages=True, manage_webhooks=True)
    @commands.guild_only()
    async def unlink_chat(self, ctx, channels: commands.Greedy[discord.TextChannel]):
        """Say goodbye to the filtered world of global chat.

Run
- %%unlink {#mention as many channels as you want (optional)}"""
        unlinked = 0
        channels = [ctx.channel] if len(channels) < 1 else channels
        for channel in channels:
            hook_status = "couldn't remove"
            if self.config.read_key(channel.id) is None:
                await ctx.send(f"The {channel.mention} channel isn't linked")
                continue
            async with aiohttp.ClientSession() as session:
                hook = discord.Webhook.from_url(self.config.read_key(channel.id)["hook"],
                                                adapter=discord.AsyncWebhookAdapter(session))
                failed = False
                try:
                    await hook.delete()
                    hook_status = "have also removed"
                except discord.Forbidden:
                    pass
                except discord.NotFound:
                    await ctx.send(f"The {channel.mention} channel isn't linked")
                    failed = True
                finally:
                    removed = self.config.remove_key(channel.id)
                    if not failed:
                        if removed:
                            unlinked += 1
                            await ctx.send(f"Unlinked the {channel.mention} channel from `{removed['channel']}`"
                                           f"(I {hook_status} the webhook)")
                        else:
                            await ctx.send(f"The {channel.mention} channel isn't linked")

        s = "" if unlinked == 1 else "s"
        await ctx.send(f"Unlinked {unlinked} channel{s}")

    @commands.command(name='get_chat', aliases=['chan', 'chat', 'getchat'])
    async def get_channel(self, ctx, channels: commands.Greedy[discord.TextChannel]):
        """Check what global chat a channel is linked to. Good for all those times you want to continue the
conversation in your own server.

Run:
- %%get_chat {#mention as many channels as you want (optional)}"""
        channels = [ctx.channel] if len(channels) < 1 else channels
        for chat in channels:
            channel = self.config.read_key(chat.id)
            if channel and channel["channel"].strip().startswith("bot-"):
                await ctx.send(f":robot: The {chat.mention} channel is linked with the bot chat `{channel['channel']}`")
            elif channel:
                await ctx.send(f":link: The {chat.mention} channel is linked with the `{channel['channel']}` chat")
            else:
                await ctx.send(f":electric_plug: The {chat.mention} channel isn't linked")
        await ctx.send("Done :white_check_mark:")


class All(commands.Cog, name="Global Moderation"):
    def __init__(self, bot):
        self.bot = bot
        self.bans = save.Save("all/bans")
        self.prefixes = save.Save("all/prefixes")

    @commands.command(name='checkban', aliases=["banned?", "banned", "ban?"])
    async def global_chat_check_ban(self, ctx, users: commands.Greedy[discord.User]):
        """Is your friend banned?

Run
- %%checkban {@mention as many users as you want (optional)}"""
        users = users if len(users) else [ctx.author]
        for user in users:
            banned = self.bans.read_key(user.id)
            if banned and (not banned.startswith("-silent") or checks.bot_mod(ctx)):
                await ctx.send(f"=> The user {user.mention} is banned for `{banned}`")
            else:
                await ctx.send(f"=> The user {user.mention} isn't banned")
        return await ctx.send("=> :white_check_mark: Done!")

    @commands.command(name='getprefix', aliases=["prefix?", "emote?"])
    async def get_prefix(self, ctx, users: commands.Greedy[discord.User]):
        """Check what your prefix is
'What's your fancy custom prefix?',
'Mine is 👑',
'Wait really?',
'Yh, and you can check'.
Run:
- %%getprefix {@mention as many users as you want (optional)}"""
        users = users if len(users) else [ctx.author]
        for user in users:
            prefix = self.prefixes.read_key(user.id)
            if prefix:
                await ctx.send(f"=> The user {user.mention} has the custom prefix `{prefix}`")
            else:
                await ctx.send(f"=> The user {user.mention} doesn't have a custom prefix")
        return await ctx.send("=> :white_check_mark: Done!")


def setup(bot):
    bot.add_cog(Chat(bot))
    bot.add_cog(All(bot))
