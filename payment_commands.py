import discord
from discord import app_commands
import sqlite3
from config import DB_PATH

def setup_payment_commands(tree):

    @tree.command(name="payer", description="Réinitialiser la balance d’un joueur après paiement en jeu")
    @app_commands.describe(user="Utilisateur à réinitialiser")
    async def payer(interaction: discord.Interaction, user: discord.Member):
        # Vérifie si l'utilisateur est admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT balance FROM user_balances WHERE user_id = ?", (user.id,))
        row = c.fetchone()

        if not row or row[0] == 0:
            await interaction.response.send_message(f"ℹ️ {user.name} n’a aucune balance à réinitialiser.", ephemeral=True)
        else:
            c.execute("UPDATE user_balances SET balance = 0 WHERE user_id = ?", (user.id,))
            conn.commit()
            await interaction.response.send_message(f"✅ La balance de **{user.name}** a été réinitialisée à 0€.", ephemeral=True)
            await interaction.channel.send(f"💸 Paiement effectué pour **{user.name}**. Sa balance a été remise à zéro.")

        conn.close()