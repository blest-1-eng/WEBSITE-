import discord
from discord.ext import commands
import requests
from io import BytesIO
from urllib.parse import quote

class Image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="image")
    async def image(self, ctx, *, prompt=None):

        if prompt is None:
            return await ctx.reply(
                "Usage:\n.image <prompt>"
            )

        msg = await ctx.reply("🎨 Generating image...")

        try:

            url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"

            r = requests.get(url, timeout=120)

            if r.status_code != 200:
                return await msg.edit(content="❌ Failed to generate image.")

            file = discord.File(
                BytesIO(r.content),
                filename="nyra.png"
            )

            embed = discord.Embed(
                title="🖼 NYRA AI IMAGE",
                description=f"**Prompt:** {prompt}",
                color=0x00ffff
            )

            embed.set_image(url="attachment://nyra.png")

            await msg.delete()

            await ctx.reply(
                embed=embed,
                file=file
            )

        except Exception as e:

            await msg.edit(content=f"❌ {e}")

async def setup(bot):
    await bot.add_cog(Image(bot))
