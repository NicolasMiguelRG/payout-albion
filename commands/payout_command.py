import discord
from discord import app_commands
from views.payout_view import PayoutView

@app_commands.command(name="payout", description="Créer un nouveau payout")
@app_commands.describe(nom="Nom du payout")
async def payout(interaction: discord.Interaction, nom: str):
    view = PayoutView(interaction.user, nom)
    await interaction.response.send_message(
        f"📦 **{nom}** créé par {interaction.user.mention}.\nSélectionne les membres à inclure dans le payout :",
        view=view,
        ephemeral=True
    )