import discord

class PayoutView(discord.ui.View):
    def __init__(self, creator, nom):
        super().__init__(timeout=None)
        self.creator = creator
        self.nom = nom
        self.selected_members = []

    @discord.ui.button(label="Valider le payout", style=discord.ButtonStyle.green)
    async def validate(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.selected_members:
            await interaction.response.send_message("⚠️ Aucun membre sélectionné.", ephemeral=True)
            return

        message = f"✅ **{self.nom}** validé par {self.creator.mention}\n\n"
        message += "**Membres sélectionnés :**\n"
        for member in self.selected_members:
            message += f"- {member.mention}\n"

        await interaction.response.send_message(message)

    @discord.ui.select(
        placeholder="Sélectionne les membres à inclure",
        min_values=1,
        max_values=25,
        options=[]  # À remplir dynamiquement si nécessaire
    )
    async def select_members(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_members = [interaction.guild.get_member(int(user_id)) for user_id in select.values]
        await interaction.response.send_message("✅ Membres sélectionnés.", ephemeral=True)