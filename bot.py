import discord
from discord.ext import commands
from config import TOKEN
from commands.payout_command import payout
from admin_commands import setup_admin_commands
from balance_commands import setup_balance_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Nécessaire pour accéder aux membres du serveur

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"📦 Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes : {e}")

# 📥 Ajout de la commande slash /payout
bot.tree.add_command(payout)

# 🛡️ Commandes admin classiques (!validate_payout, !delete_payout, !list_payouts)
setup_admin_commands(bot)

# 💰 Commandes de solde (!bal, !bl)
setup_balance_commands(bot)

# 🔐 Vérification du token
if not TOKEN:
    raise ValueError("❌ Le token Discord est vide ou non défini. Vérifie ta variable d'environnement 'TOKEN'.")

# 🚀 Démarrage du bot
bot.run(TOKEN)