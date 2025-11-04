import discord
from discord.ext import commands
from commands.payout_command import payout

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

# 📥 Ajout de la commande /payout
bot.tree.add_command(payout)

bot.run(TOKEN)