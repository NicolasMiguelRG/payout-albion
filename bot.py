import discord
from discord.ext import commands
from commands.payout_command import PayoutCommand

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Nécessaire pour accéder aux membres du serveur

bot = commands.Bot(command_prefix="!", intents=intents)
tree = discord.app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await tree.sync()
        print(f"📦 Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation : {e}")

# 📥 Ajout de la commande /payout
tree.add_command(PayoutCommand(bot).payout)

# 🟢 Démarrage du bot
bot.run("TON_TOKEN_ICI")