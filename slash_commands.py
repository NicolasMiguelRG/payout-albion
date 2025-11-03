from discord import app_commands, Interaction
from modals import PayoutModal

def setup_slash_commands(tree):
    @tree.command(name="payout", description="Créer un payout interactif")
    @app_commands.describe(name="Nom du payout")
    async def payout(interaction: Interaction, name: str):
        await interaction.response.send_modal(PayoutModal(name))