import os
import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def reload(self, ctx):

        loaded = []

        for ext in list(self.bot.extensions):

            try:
                await self.bot.reload_extension(ext)
                loaded.append(ext)

            except Exception as e:
                await ctx.reply(f"❌ {ext}\n{e}")
                return

        await ctx.reply("✅ Reload Complete")

    @commands.command()
    async def sync(self, ctx):

        synced = await self.bot.tree.sync()

        await ctx.reply(f"✅ Synced {len(synced)} Slash Commands")

    @commands.command()
    async def shutdown(self, ctx):

        await ctx.reply("👋 Shutting Down...")

        await self.bot.close()

    @commands.command()
    async def restart(self, ctx):

        await ctx.reply("♻ Restarting...")

        os.execv(
            os.sys.executable,
            ["python"] + os.sys.argv
        )

async def setup(bot):
    await bot.add_cog(Owner(bot))
