import discord
import sqlite3

class PayoutModal(discord.ui.Modal, title="Créer un payout"):

    def __init__(self, payout_name: str, caller_name: str):
        super().__init__()
        self.payout_name = payout_name
        self.caller_name = caller_name

        self.total = discord.ui.TextInput(label="Prix total", placeholder="Ex: 1 000 000", required=True)
        self.repairs = discord.ui.TextInput(label="Réparations", placeholder="Ex: 200 000", required=True)
        self.members = discord.ui.TextInput(label="Membres", placeholder="Ex: 5", required=True)
        self.guild = discord.ui.TextInput(label="Membre guilde ? (oui/non)", placeholder="oui", required=True)
        self.percent = discord.ui.TextInput(label="% pour la guilde", placeholder="Ex: 10", required=True)

        self.add_item(self.total)
        self.add_item(self.repairs)
        self.add_item(self.members)
        self.add_item(self.guild)
        self.add_item(self.percent)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            total = int(self.total.value.replace(" ", ""))
            repairs = int(self.repairs.value.replace(" ", ""))
            members = int(self.members.value)
            is_guild = self.guild.value.lower() == "oui"
            percent = int(self.percent.value)

            guild_cut = int((total - repairs) * percent / 100) if is_guild else 0
            net = total - repairs - guild_cut
            per_member = int(net / members)

            # ✅ Connexion sécurisée à SQLite
            try:
                with sqlite3.connect("payouts.db") as conn:
                    c = conn.cursor()
                    c.execute('''
                        INSERT INTO payouts (name, caller, total, repairs, guild_percent, guild_cut, net, per_member)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        self.payout_name,
                        self.caller_name,
                        total,
                        repairs,
                        percent,
                        guild_cut,
                        net,
                        per_member
                    ))
                    conn.commit()
            except sqlite3.IntegrityError as e:
                msg = f"❌ Erreur : le nom '{self.payout_name}' existe déjà."
                if interaction.response.is_done():
                    await interaction.followup.send(msg, ephemeral=True)
                else:
                    await interaction.response.send_message(msg, ephemeral=True)
                return
            except sqlite3.OperationalError as e:
                msg = f"❌ Erreur base de données : {e}"
                if interaction.response.is_done():
                    await interaction.followup.send(msg, ephemeral=True)
                else:
                    await interaction.response.send_message(msg, ephemeral=True)
                return

            # ✅ Message public dans le salon
            try:
                await interaction.channel.send(
                    f"💰 Payout **{self.payout_name}** lancé par **{self.caller_name}**\n"
                    f"Total : {total:,} • Réparations : {repairs:,}\n"
                    f"Guilde : {guild_cut:,} • Net : {net:,} • Par membre : {per_member:,}"
                )
            except discord.Forbidden:
                await interaction.followup.send(
                    "⚠️ Je n’ai pas les permissions pour envoyer un message public dans ce salon.",
                    ephemeral=True
                )
                return

            # ✅ Confirmation privée
            if interaction.response.is_done():
                await interaction.followup.send("✅ Payout enregistré avec succès.", ephemeral=True)
            else:
                await interaction.response.send_message("✅ Payout enregistré avec succès.", ephemeral=True)

        except Exception as e:
            msg = f"❌ Erreur inattendue : {e}"
            if interaction.response.is_done():
                await interaction.followup.send(msg, ephemeral=True)
            else:
                await interaction.response.send_message(msg, ephemeral=True)