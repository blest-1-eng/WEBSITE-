import asyncio
import discord
from discord.ext import commands
import config

TOKEN = config.DISCORD_TOKEN

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

COGS = [
    "discord.chat",
    "discord.events",
    "discord.admin",
]


@bot.event
async def on_ready():
    print("=" * 50)
    print("🤖 NYRA Discord Bot Online")
    print(f"Logged in as : {bot.user}")
    print(f"User ID      : {bot.user.id}")
    print(f"Servers      : {len(bot.guilds)}")
    print("=" * 50)

    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash Commands Synced : {len(synced)}")
    except Exception as e:
        print(e)


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        return

    print(f"[ERROR] {error}")


async def load_cogs():

    for cog in COGS:

        try:

            await bot.load_extension(cog)

            print(f"✅ Loaded -> {cog}")

        except Exception as e:

            print(f"❌ Failed -> {cog}")

            print(e)


async def main():

    async with bot:

        await load_cogs()

        await bot.start(TOKEN)


if __name__ == "__main__":

    asyncio.run(main())
