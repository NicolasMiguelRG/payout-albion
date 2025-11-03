import discord
from discord.ext import commands
from config import TOKEN
from database import init_db
from text_commands import setup_text_commands
from admin_commands import setup_admin_commands
from payment_commands import setup_payment_commands  # ← AJOUT ICI

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    init_db()
    setup_text_commands(bot)
    setup_admin_commands(bot)
    setup_payment_commands(bot.tree)  # ← AJOUT ICI
    await bot.tree.sync()
    print(f"✅ Connecté en tant que {bot.user}")

async def main():
    await bot.load_extension("slash_commands")  # ← Charge ton Cog slash
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())