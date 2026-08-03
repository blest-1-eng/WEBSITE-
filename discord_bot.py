import asyncio
import discord
from discord.ext import commands
import config
from discord.config_manager import load

TOKEN = config.DISCORD_TOKEN

intents = discord.Intents.all()


def get_prefix(bot, message):
    try:
        return load()["prefix"]
    except Exception:
        return "!"


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    help_command=None
)

# AI channel reference
bot.ai_channel = None


COGS = [
    "discord.chat",
    "discord.events",
    "discord.admin",
    "discord.general",
    "discord.owner",
    "discord.image",
    "discord.pdf_ai"
]


@bot.event
async def on_ready():
    print("=" * 50)
    print("🤖 NYRA Discord Bot Online")
    print(f"Logged in as : {bot.user}")
    print(f"User ID      : {bot.user.id}")
    print(f"Servers      : {len(bot.guilds)}")
    print("=" * 50)

    # Save AI channel object
    try:
        data = load()
        bot.ai_channel = bot.get_channel(data["ai_channel"])
    except Exception:
        bot.ai_channel = None

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
