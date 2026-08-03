import discord
from discord.ext import commands
from discord import app_commands
from discord.config_manager import load
from datetime import datetime


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ping")
    async def ping(self, ctx):

        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 NYRA • Pong",
            description=f"```yaml\nLatency : {latency} ms\n```",
            color=0x0B3D91
        )

        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )

        embed.set_footer(
            text="NYRA AI • Made by Akshat"
        )

        embed.timestamp = datetime.utcnow()

        await ctx.reply(embed=embed)


    @commands.command(name="help")
    async def help_prefix(self, ctx):

        data = load()

        prefix = data["prefix"]

        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(

            title="🤖 NYRA AI",

            description=(
                "**Personal AI Discord Assistant**\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),

            color=0x0B3D91

        )

        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )

        embed.add_field(

            name="🧠 AI COMMANDS",

            value=(
                f"💬 `{prefix}nyra <message>`\n"
                f"🖼️ `{prefix}image <prompt>`"
            ),

            inline=False

        )

        embed.add_field(

            name="⚙️ GENERAL",

            value=(
                f"📖 `{prefix}help`\n"
                f"🏓 `{prefix}ping`\n"
                f"📚 `/help`"
            ),

            inline=False

        )

        embed.add_field(

            name="👑 OWNER",

            value=(
                f"♻️ `{prefix}reload`\n"
                f"📡 `{prefix}sync`\n"
                f"🔄 `{prefix}restart`\n"
                f"⛔ `{prefix}shutdown`"
            ),

            inline=False

        )

        embed.add_field(

            name="🌐 SYSTEM",

            value=(
                f"**Prefix :** `{prefix}`\n"
                f"**Latency :** `{latency} ms`\n"
                f"**Version :** `NYRA V2`\n"
                f"**Library :** `discord.py 2.7.1`"
            ),

            inline=False

        )
        embed.set_footer(
            text="NYRA V2 • Made by Akshat"
        )

        embed.timestamp = datetime.utcnow()

        await ctx.reply(embed=embed)


    @app_commands.command(
        name="help",
        description="Show Nyra Help Menu"
    )
    async def help_slash(self, interaction: discord.Interaction):

        data = load()

        prefix = data["prefix"]

        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(

            title="🤖 NYRA AI",

            description=(
                "**Personal AI Discord Assistant**\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),

            color=0x0B3D91

        )

        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )

        embed.add_field(

            name="🧠 AI COMMANDS",

            value=(
                f"💬 `{prefix}nyra <message>`\n"
                f"🖼️ `{prefix}image <prompt>`"
            ),

            inline=False

        )

        embed.add_field(

            name="⚙️ GENERAL",

            value=(
                f"📖 `{prefix}help`\n"
                f"🏓 `{prefix}ping`\n"
                f"📚 `/help`"
            ),

            inline=False

        )

        embed.add_field(

            name="👑 OWNER",

            value=(
                f"♻️ `{prefix}reload`\n"
                f"📡 `{prefix}sync`\n"
                f"🔄 `{prefix}restart`\n"
                f"⛔ `{prefix}shutdown`"
            ),

            inline=False

        )

        embed.add_field(

            name="🌐 SYSTEM",

            value=(
                f"**Prefix :** `{prefix}`\n"
                f"**Latency :** `{latency} ms`\n"
                f"**Version :** `NYRA V2`\n"
                f"**Library :** `discord.py 2.7.1`"
            ),

            inline=False

        )
        embed.set_footer(
            text="NYRA V2 • Made by Akshat"
        )

        embed.timestamp = datetime.utcnow()

        await ctx.reply(embed=embed)


    @app_commands.command(
        name="help",
        description="Show Nyra Help Menu"
    )
    async def help_slash(self, interaction: discord.Interaction):

        data = load()

        prefix = data["prefix"]

        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(

            title="🤖 NYRA AI",

            description=(
                "**Personal AI Discord Assistant**\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),

            color=0x0B3D91

        )

        embed.set_thumbnail(
            url=self.bot.user.display_avatar.url
        )

        embed.add_field(

            name="🧠 AI COMMANDS",

            value=(
                f"💬 `{prefix}nyra <message>`\n"
                f"🖼️ `{prefix}image <prompt>`"
            ),

            inline=False

        )

        embed.add_field(

            name="⚙️ GENERAL",

            value=(
                f"📖 `{prefix}help`\n"
                f"🏓 `{prefix}ping`\n"
                f"📚 `/help`"
            ),

            inline=False

        )

        embed.add_field(

            name="👑 OWNER",

            value=(
                f"♻️ `{prefix}reload`\n"
                f"📡 `{prefix}sync`\n"
                f"🔄 `{prefix}restart`\n"
                f"⛔ `{prefix}shutdown`"
            ),

            inline=False

        )

        embed.add_field(

            name="🌐 SYSTEM",

            value=(
                f"**Prefix :** `{prefix}`\n"
                f"**Latency :** `{latency} ms`\n"
                f"**Version :** `NYRA V2`\n"
                f"**Library :** `discord.py 2.7.1`"
            ),

            inline=False

        )

        embed.set_footer(
            text="NYRA V2 • Made by Akshat"
        )

        embed.timestamp = datetime.utcnow()

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(General(bot))
