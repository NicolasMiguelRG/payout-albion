from discord import app_commands, Interaction
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="payout", description="Créer un payout avec nom et caller")
    @app_commands.describe(
        nom_payout="Nom du payout",
        nom_caller="Nom du joueur qui appelle le payout"
    )
    async def payout(self, interaction: Interaction, nom_payout: str, nom_caller: str):
        # Traitement ici — tu peux enregistrer le payout dans ta base ou afficher un résumé
        await interaction.response.send_message(
            f"Payout **{nom_payout}** lancé par **{nom_caller}** 🎉",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(SlashCommands(bot))