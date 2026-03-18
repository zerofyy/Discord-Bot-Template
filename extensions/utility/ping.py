from discord.ext import commands

from utils.extension_manager import Command


@Command(name = 'ping', description = 'Extensions test')
async def command(ctx: commands.Context) -> None:
    await ctx.send('Pong!')
