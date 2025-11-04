import discord
from discord import app_commands
from views.payout_view import PayoutView

class PayoutCommand(discord.app_commands.CommandTree):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    @app_commands.command(name="payout", description="Créer un nouveau payout")
    async def payout(self, interaction: discord.Interaction):
        view = PayoutView(caller_name=interaction.user.name)
        await interaction.response.send_message("🧾 Sélectionne les membres du payout :", view=view, ephemeral=True)