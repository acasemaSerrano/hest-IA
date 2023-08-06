from discord.ext import commands
from discord.ext.commands import Context
import os
import discord

class OpenAI(commands.Cog, name="OpenAI"):
    def __init__(self, bot):
        self.bot = bot

    ruta = os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", "OpenAI.prompt.txt")

    @commands.hybrid_command(
        name="getprompt",
        description="Te escribe todo el prompt usado hasta el momento",
    )
    async def getprompt(self, context: Context):
        global ruta

        if not os.path.exists(ruta):
            context.send('Error, El fichero no existe')
            return

        with open(ruta, encoding="utf-8") as file:

            embed = discord.Embed(
                description="Prompt usado para GPT",
                color=0x9C84EF
            )

            embed = embed.add_field(
                name="Prompt:",
                value=file.read(),
                inline=True
            )

            embed.set_footer(
                text=f"Requested by {context.author}"
            )
            await context.send(embed=embed)


    @commands.hybrid_command(
        name="setprompt",
        description="Te permite modificar el prompt",
    )
    async def setprompt(self, context: Context):
        global ruta

        if not os.path.exists(ruta):
            context.send('Error, El fichero no existe')
            return
        

        with open(ruta, "w", encoding="utf-8") as file:

            file.truncate(0)
            file.write(context.message.content.replace("/setprompt ", ""))
            file.closed
            context.send('Cambio realizado correctamente')


async def setup(bot):
    await bot.add_cog(OpenAI(bot))     