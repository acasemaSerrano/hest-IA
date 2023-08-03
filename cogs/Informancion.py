import platform
import os

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Informancion(commands.Cog, name="Informancion"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="botinfo",
        description="Obtenga información útil (o no) sobre el bot.",
    )
    async def botinfo(self, context: Context) -> None:
        embed = discord.Embed(
            description="Hola soy Hest-IA",
            color=0x9C84EF
        )
        embed.set_author(
            name="Desarrollador acasema"
        )
        embed.add_field(
            name="Creador:",
            value="acasema",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Barra) o {self.bot.config['prefix']} para comandos normales",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        await context.send(embed=embed)

    @commands.command(
        name="serverinfo",
        description="Obtenga información útil (o no) sobre el servidor.",
    )
    async def serverinfo(self, context: Context) -> None:
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0x9C84EF
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.command(
        name="ping",
        description="Compruebe si el bot está vivo.",
    )
    async def ping(self, context: Context) -> None:
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    def changelogMulti(solo1: bool):

        textFile = open(f"{os.path.realpath(os.path.dirname(__file__))}/../changelog.md", encoding="utf-8").read()
        infoVersios = textFile.split("##")
        embed = discord.Embed(
            title="Changelog",
            color=0x9C84EF
        )
        
        for i in range(1, len(infoVersios)):

            VInfo = infoVersios[i].split('\n')
            VNumero = VInfo[0][VInfo[0].find('[')+1:VInfo[0].find(']')]

            title = "**" +  VNumero + "**"
            VInfo.pop(0)
            text = str.join("\n", VInfo)

            embed = embed.add_field(
                name=title,
                value=text,
                inline=False
            )
            if solo1==True:
                break
                

        UVInfo = infoVersios[1].split('\n')[0]
        UVNumero = UVInfo[UVInfo.find('[')+1:UVInfo.find(']')]
        embed.set_footer(
            text=f"Version actual {UVNumero}"
        )
        return embed
    

    @commands.group(
        invoke_without_command=True,
        name="changelog",
        description="Proporciona el último cambio que ha habido",
    )
    async def changelog(self, context: Context):
        await context.send(embed=Informancion.changelogMulti(True))

    @changelog.command(name="all", description="Todos los cambios registrados")        
    async def changelog_all(self, context: Context):
        await context.send(embed=Informancion.changelogMulti(False))



async def setup(bot):
    await bot.add_cog(Informancion(bot))
