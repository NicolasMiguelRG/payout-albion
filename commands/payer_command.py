import discord
import sqlite3
from discord import app_commands
from config import DB_PATH

@app_commands.command(name="payer", description="Effectue le paiement d'un joueur et réinitialise sa balance")
@app_commands.describe(membre="Le joueur à payer")
async def payer(interaction: discord.Interaction, membre: discord.Member):
    user_id = membre.id

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT balance FROM user_balances WHERE user_id = ?", (user_id,))
        row = c.fetchone()

        if not row or row[0] == 0:
            await interaction.response.send_message(f"💸 {membre.display_name} n'a aucune balance à payer.", ephemeral=True)
            return

        montant = row[0]

        # Réinitialiser la balance
        c.execute("UPDATE user_balances SET balance = 0 WHERE user_id = ?", (user_id,))

        # Recalculer les pièces en circulation
        c.execute("SELECT SUM(balance) FROM user_balances")
        total_row = c.fetchone()
        total = total_row[0] if total_row and total_row[0] else 0

        conn.commit()

    await interaction.response.send_message(
        f"✅ Paiement effectué pour **{membre.display_name}** : {montant:,} pièces.\n"
        f"💰 Pièces restantes en circulation : {total:,} pièces."
    )