import discord
from discord.ext import commands
from config import TOKEN
from database import init_db
from slash_commands import setup_slash_commands
from text_commands import setup_text_commands
from admin_commands import setup_admin_commands
from payment_commands import setup_payment_commands  # ← AJOUT ICI

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    init_db()
    setup_slash_commands(tree)
    setup_text_commands(bot)
    setup_admin_commands(bot)
    setup_payment_commands(tree)  # ← AJOUT ICI
    await tree.sync()
    print(f"✅ Connecté en tant que {bot.user}")

bot.run(TOKEN)