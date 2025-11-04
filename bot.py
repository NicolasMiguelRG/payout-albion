import discord
from discord.ext import commands
from config import TOKEN
from commands.payout_command import payout
from admin_commands import setup_admin_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"📦 Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation : {e}")

bot.tree.add_command(payout)
setup_admin_commands(bot)

if not TOKEN:
    raise ValueError("❌ Le token Discord est vide ou non défini. Vérifie ta variable d'environnement 'TOKEN'.")

bot.run(TOKEN)