from discord import app_commands, Interaction
from modals import PayoutModal

def setup_slash_commands(tree: app_commands.CommandTree):
    @tree.command(name="payout", description="Créer un payout interactif")
    @app_commands.describe(
        name="Nom du payout",
        caller="Nom du joueur qui appelle le payout"
    )
    async def payout(interaction: Interaction, name: str, caller: str):
        # Ouvre le modal avec les deux paramètres
        await interaction.response.send_modal(PayoutModal(name, caller))