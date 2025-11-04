import discord
from discord import app_commands
from views.payout_view import PayoutView

@app_commands.command(name="payout", description="Créer un nouveau payout")
async def payout(interaction: discord.Interaction):
    view = PayoutView(caller_name=interaction.user.name)
    await interaction.response.send_message(
        "🧾 Sélectionne les membres du payout puis clique sur **Valider le payout** :",
        view=view,
        ephemeral=True
    )