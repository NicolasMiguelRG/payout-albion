import discord
from discord.ext import commands
from config import TOKEN
from commands.payout_command import payout
from commands.payer_command import payer
from admin_commands import setup_admin_commands
from balance_commands import setup_balance_commands

# Remplace par l'ID de ton serveur Discord
GUILD_ID = 123456789012345678  # ← à personnaliser

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"📦 Commandes slash synchronisées localement : {len(synced)}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes : {e}")

# 📥 Commandes slash
bot.tree.add_command(payout)
bot.tree.add_command(payer)

# 🛡️ Commandes classiques
setup_admin_commands(bot)
setup_balance_commands(bot)

# 🔐 Vérification du token
if not TOKEN:
    raise ValueError("❌ Le token Discord est vide ou non défini. Vérifie ta variable d'environnement 'TOKEN'.")

# 🚀 Démarrage du bot
bot.run(TOKEN)