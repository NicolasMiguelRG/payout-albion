import discord
from discord.ext import commands
from config import TOKEN
from database import init_db
from text_commands import setup_text_commands
from admin_commands import setup_admin_commands
from payment_commands import setup_payment_commands
from slash_commands import setup_slash_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    init_db()  # Initialise la base de données
    setup_text_commands(bot)  # Commandes textuelles (!bal, !bl, etc.)
    setup_admin_commands(bot)  # Commandes admin (!validate_payout, etc.)
    setup_payment_commands(bot.tree)  # Commandes slash liées aux paiements
    setup_slash_commands(bot.tree)  # Commande slash /payout
    await bot.tree.sync()  # Synchronise les commandes slash avec Discord
    print(f"✅ Connecté en tant que {bot.user}")

bot.run(TOKEN)