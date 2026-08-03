import asyncio
import discord
from discord.ext import commands
from modules.brain import reply
from discord.config_manager import load


class Chat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def lock_ai_channel(self, channel, seconds):
        overwrite = channel.overwrites_for(channel.guild.default_role)
        overwrite.send_messages = False

        await channel.set_permissions(
            channel.guild.default_role,
            overwrite=overwrite
        )

        await channel.send(
            f"🔒 Nyra AI temporarily unavailable.\n"
            f"Please wait about {seconds // 60} minutes."
        )

        await asyncio.sleep(seconds)

        overwrite.send_messages = None

        await channel.set_permissions(
            channel.guild.default_role,
            overwrite=overwrite
        )

        await channel.send("🔓 Nyra AI is back online.")

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        data = load()
        prefix = data["prefix"]

        if message.content.startswith(prefix):
            await self.bot.process_commands(message)
            return

        if data["ai_channel"] == message.channel.id:

            async with message.channel.typing():

                try:
                    answer = reply(message.content)

                    if answer == "__RATE_LIMIT__":
                        from modules.ai import AI_COOLDOWN

                        await self.lock_ai_channel(
                            message.channel,
                            AI_COOLDOWN["retry_after"]
                        )
                        return

                except Exception as e:
                    answer = f"❌ {e}"

            if not answer:
                answer = "I couldn't generate a reply."

            answer = str(answer)

            if len(answer) > 1900:
                answer = answer[:1900]

            await message.reply(answer)

        await self.bot.process_commands(message)

    @commands.command(name="nyra")
    async def nyra(self, ctx, *, text=None):

        if text is None:
            return await ctx.reply(
                f"Usage:\n{load()['prefix']}nyra <message>"
            )

        async with ctx.typing():

            try:
                answer = reply(text)

                if answer == "__RATE_LIMIT__":
                    from modules.ai import AI_COOLDOWN

                    await self.lock_ai_channel(
                        ctx.channel,
                        AI_COOLDOWN["retry_after"]
                    )
                    return

            except Exception as e:
                answer = f"❌ {e}"

        await ctx.reply(answer)


async def setup(bot):
    await bot.add_cog(Chat(bot))
