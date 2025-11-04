import discord
import sqlite3

class PayoutView(discord.ui.View):
    def __init__(self, caller_name: str):
        super().__init__(timeout=300)
        self.caller_name = caller_name
        self.selected_members = []

    @discord.ui.select(cls=discord.ui.UserSelect, placeholder="👥 Sélectionne les membres", min_values=1, max_values=10)
    async def select_members(self, interaction: discord.Interaction, select: discord.ui.UserSelect):
        self.selected_members = select.values
        await interaction.response.send_message("✅ Membres sélectionnés.", ephemeral=True)

    @discord.ui.button(label="Valider le payout", style=discord.ButtonStyle.green)
    async def validate(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PayoutDetailsModal(self.caller_name, self.selected_members)
        await interaction.response.send_modal(modal)


class PayoutDetailsModal(discord.ui.Modal, title="Détails du payout"):
    def __init__(self, caller_name, members):
        super().__init__()
        self.caller_name = caller_name
        self.members = members

        self.total = discord.ui.TextInput(label="Prix total", placeholder="Ex: 1 000 000", required=True)
        self.repairs = discord.ui.TextInput(label="Réparations", placeholder="Ex: 200 000", required=True)
        self.guild = discord.ui.TextInput(label="Part de guilde ? (oui/non)", placeholder="oui", required=True)
        self.percent = discord.ui.TextInput(label="% vente Tab ! (FDP OKIMI)", placeholder="Ex: 10", required=True)

        self.add_item(self.total)
        self.add_item(self.repairs)
        self.add_item(self.guild)
        self.add_item(self.percent)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            total = int(self.total.value.replace(" ", ""))
            repairs = int(self.repairs.value.replace(" ", ""))
            percent = int(self.percent.value)
            is_guild = self.guild.value.lower() == "oui"

            members = len(self.members)
            guild_cut = int((total - repairs) * percent / 100) if is_guild else 0
            net = total - repairs - guild_cut
            per_member = int(net / members) if members > 0 else 0

            payout_name = f"Payout-{interaction.id}"

            with sqlite3.connect("payouts.db") as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO payouts (name, caller, total, repairs, guild_percent, guild_cut, net, per_member)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    payout_name,
                    self.caller_name,
                    total,
                    repairs,
                    percent,
                    guild_cut,
                    net,
                    per_member
                ))

                for member in self.members:
                    user_id = member.id
                    c.execute('''
                        INSERT INTO user_balances (user_id, balance)
                        VALUES (?, ?)
                        ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?
                    ''', (user_id, per_member, per_member))

                    c.execute('''
                        INSERT INTO payout_users (payout_name, user_id)
                        VALUES (?, ?)
                    ''', (payout_name, user_id))

                conn.commit()

            mentions = ", ".join([m.mention for m in self.members])
            await interaction.channel.send(
                f"💰 **Payout {payout_name}** lancé par **{self.caller_name}**\n"
                f"👥 Membres : {mentions}\n"
                f"💸 Total : {total:,} • Réparations : {repairs:,}\n"
                f"🏰 Guilde : {guild_cut:,} • Net : {net:,} • Par membre : {per_member:,}"
            )

            await interaction.response.send_message("✅ Payout enregistré et distribué avec succès.", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur : {e}", ephemeral=True)