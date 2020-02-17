import asyncio

import discord
from discord.ext import commands


# Define commonly used functions. We use a single underscore ('_') to let people know that we shouldn't access this
# outside of this module but still allow it
def bot_mod(ctx):
    mod_users = []
    mod_roles = [625584831320948737]
    if ctx.author is None:
        return False
    if ctx.author.id in mod_users:
        return True
    if ctx.author.id in ctx.bot.admins:
        return True
    mods = []
    for role in mod_roles:
        mods = mods + discord.utils.get(
            ctx.bot.get_guild(606866057998762023).roles, id=role).members
    mod_ids = []
    for mod in mods:
        mod_ids.append(mod.id)
    if ctx.author.id in mod_ids:
        return True
    return False


def is_owner(ctx):
    if ctx.author.id in ctx.bot.admins:
        return True
    return False


def tester(ctx):
    testers = []
    test_roles = [606990137275973635]
    if ctx.author is None:
        return False
    if ctx.author in testers:
        return True
    testers = []
    for role in test_roles:
        testers = testers + discord.utils.get(
            ctx.bot.get_guild(606866057998762023).roles, id=role).members
    test_ids = []
    for test in testers:
        test_ids.append(test.id)
    if ctx.author.id in test_ids:
        return True
    return False


def intestingserver(ctx):
    try:
        if ctx.author in ctx.bot.get_guild(413314727591149568).members:
            return True
        return False
    except AttributeError:
        return False


def inbetaserver(ctx):
    if ctx.author in ctx.bot.get_guild(606866057998762023).members:
        return True
    return False