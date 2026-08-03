from discord.ext import commands
from discord.config_manager import load, save
import discord

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx):

        data = load()
        data["ai_channel"] = ctx.channel.id
        save(data)

        await ctx.send(f"✅ AI Channel set to {ctx.channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix):

        data = load()
        data["prefix"] = prefix
        save(data)

        await ctx.send(f"✅ Prefix changed to `{prefix}`")

    @commands.command()
    async def panel(self, ctx):

        data = load()

        embed = discord.Embed(
            title="NYRA Admin Panel",
            color=0x00ffff
        )

        embed.add_field(
            name="Prefix",
            value=data["prefix"],
            inline=False
        )

        embed.add_field(
            name="AI Channel",
            value=data["ai_channel"],
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
