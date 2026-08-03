from discord.ext import commands
from modules.brain import reply
from discord.config_manager import load

class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        data = load()

        # Dedicated AI Channel
        if data["ai_channel"] == message.channel.id:

            async with message.channel.typing():

                try:
                    answer = reply(message.content)

                except Exception as e:
                    answer = f"❌ {e}"

            if answer is None:
                answer = "I couldn't generate a reply."

            answer = str(answer)

            if len(answer) > 1900:
                answer = answer[:1900]

            await message.reply(answer)

        await self.bot.process_commands(message)

    @commands.command(name="nyra")
    async def nyra(self, ctx, *, text=None):

        if text is None:
            return await ctx.reply("Usage:\n!nyra <message>")

        async with ctx.typing():

            try:
                answer = reply(text)

            except Exception as e:
                answer = f"❌ {e}"

        await ctx.reply(answer)


async def setup(bot):
    await bot.add_cog(Chat(bot))
