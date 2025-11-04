import discord
from discord.ext import commands
from config import TOKEN
from commands.payout_command import payout
from commands.payer_command import payer
from admin_commands import setup_admin_commands
from balance_commands import setup_balance_commands

# Remplace par l'ID de ton serveur Discord
GUILD_ID = 1250974626197278771  # ← à personnaliser

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.clear_commands(guild=guild)  # pas de await ici
        synced = await bot.tree.sync(guild=guild)
        print(f"📦 Commandes slash resynchronisées : {len(synced)}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation : {e}")

# 📥 Commandes slash
bot.tree.add_command(payout)
bot.tree.add_command(payer)

# 🛡️ Commandes classiques
setup_admin_commands(bot)
setup_balance_commands(bot)

# 🧼 Commande de reset (à supprimer une fois que tout fonctionne)
@bot.command(name="reset_commands")
async def reset_commands(ctx):
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild
        bot.tree.clear_commands(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        await ctx.send(f"✅ Commandes slash réinitialisées pour le serveur : {guild.name}")
    else:
        await ctx.send("❌ Tu dois être admin pour exécuter cette commande.")

# 🔐 Vérification du token
if not TOKEN:
    raise ValueError("❌ Le token Discord est vide ou non défini. Vérifie ta variable d'environnement 'TOKEN'.")

# 🚀 Démarrage du bot
bot.run(TOKEN)