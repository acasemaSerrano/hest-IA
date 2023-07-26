import pyjokes
import random

from discord.ext import commands
from discord.ext.commands import Context


class Funny(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="chiste",
        description="Proporciona un chiste",
    )
    async def chiste(self, context: Context):
        joke = pyjokes.get_jokes( language='es', category='all')
        await context.send(f"""{context.author.mention}: {random.choice(joke)}""")


async def setup(bot):
    await bot.add_cog(Funny(bot))
