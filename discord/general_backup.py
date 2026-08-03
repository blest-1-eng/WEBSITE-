import discord
from discord.ext import commands
from discord import app_commands
from discord.config_manager import load


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ping")
    async def ping(self, ctx):

        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**Latency:** `{latency} ms`",
            color=0x00ffff
        )

        embed.set_footer(
            text="NYRA AI • Made by Akshat"
        )

        await ctx.reply(embed=embed)


    @commands.command(name="help")
    async def help_prefix(self, ctx):

        data = load()
        prefix = data["prefix"]

        embed = discord.Embed(
            title="🤖 NYRA AI",
            description="### Available Commands",
            color=0x00ffff
        )

        embed.add_field(
            name="🧠 AI",
            value=(
                f"`{prefix}nyra <message>`\n"
                f"`{prefix}image <prompt>`"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ General",
            value=(
                f"`{prefix}help`\n"
                f"`/help`\n"
                f"`{prefix}ping`"
            ),
            inline=False
        )

        embed.add_field(
            name="👑 Owner",
            value=(
                f"`{prefix}reload`\n"
                f"`{prefix}sync`\n"
                f"`{prefix}restart`\n"
                f"`{prefix}shutdown`"
            ),
            inline=False
        )

        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )

        embed.set_footer(
            text=f"Prefix : {prefix} • NYRA V2 • Made by Akshat"
        )

        await ctx.reply(embed=embed)


    @app_commands.command(
        name="help",
        description="Show Nyra Help Menu"
    )
    async def help_slash(self, interaction: discord.Interaction):

        data = load()
        prefix = data["prefix"]

        embed = discord.Embed(
            title="🤖 NYRA AI",
            description="### Available Commands",
            color=0x00ffff
        )

        embed.add_field(
            name="🧠 AI",
            value=(
                f"`{prefix}nyra <message>`\n"
                f"`{prefix}image <prompt>`"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ General",
            value=(
                f"`{prefix}help`\n"
                f"`/help`\n"
                f"`{prefix}ping`"
            ),
            inline=False
        )

        embed.add_field(
            name="👑 Owner",
            value=(
                f"`{prefix}reload`\n"
                f"`{prefix}sync`\n"
                f"`{prefix}restart`\n"
                f"`{prefix}shutdown`"
            ),
            inline=False
        )

        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )

        embed.set_footer(
            text=f"Prefix : {prefix} • NYRA V2 • Made by Akshat"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(General(bot))
