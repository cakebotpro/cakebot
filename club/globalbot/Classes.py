from utils import checks, save

class Author:
    def __init__(self, ctx, anon=False):
        self.author = ctx.author
        self.avatar_url = ctx.author.avatar_url
        self.name = str(ctx.author)
        self.id = ctx.author.id
        self.emote = "👤"
        self._emote = self.emote
        self.prefixes = save.Save("all/prefixes")
        self.custom = self.prefixes.read_key(ctx.author.id)
        if ctx.author.id in ctx.bot.admins:
            self.setemote("👑")
        elif checks.bot_mod(ctx):
            self.setemote("🔨")
        elif checks.tester(ctx):
            self.setemote("🧰")
        elif checks.intestingserver(ctx):
            self.setemote("🔧")
        elif checks.inbetaserver(ctx):
            self.setemote("🐉")
        if self.custom:
            self.setcustomemote(self.custom)
        if anon:
            self.anon()

    def setemote(self, emote):
        self.emote = emote
        self._emote = self.emote

    def setcustomemote(self, emote):
        self.emote = emote

    def __repr__(self):
        return self.name

    def anon(self):
        self.avatar_url = self.author.default_avatar_url
        self.name = "???"
        self.id = "Unknown ID"
        self.emote = "❓"

    def un_anon(self):
        self.avatar_url = self.author.avatar_url
        self.name = str(self.author)
        self.id = self.author.id
        self.emote = self._emote
