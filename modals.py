import discord
import sqlite3

class PayoutModal(discord.ui.Modal, title="Créer un payout"):

    def __init__(self, payout_name: str, caller_name: str):
        super().__init__()
        self.payout_name = payout_name
        self.caller_name = caller_name

        self.total = discord.ui.TextInput(label="Prix total", placeholder="Ex: 1 000 000", required=True)
        self.repairs = discord.ui.TextInput(label="Réparations", placeholder="Ex: 200 000", required=True)
        self.members = discord.ui.TextInput(label="Membres (mentions séparées par virgule)", placeholder="@joueur1, @joueur2", required=True)
        self.guild = discord.ui.TextInput(label="Part de guilde ? (oui/non)", placeholder="oui", required=True)
        self.percent = discord.ui.TextInput(label="% vente Tab ! (FDP OKIMI)", placeholder="Ex: 10", required=True)

        self.add_item(self.total)
        self.add_item(self.repairs)
        self.add_item(self.members)
        self.add_item(self.guild)
        self.add_item(self.percent)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            total = int(self.total.value.replace(" ", ""))
            repairs = int(self.repairs.value.replace(" ", ""))
            percent = int(self.percent.value)
            is_guild = self.guild.value.lower() == "oui"

            members_raw = self.members.value
            members_list = [m.strip() for m in members_raw.split(",") if m.strip()]
            members = len(members_list)

            guild_cut = int((total - repairs) * percent / 100) if is_guild else 0
            net = total - repairs - guild_cut
            per_member = int(net / members) if members > 0 else 0

            # Enregistrement du payout
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
            except sqlite3.IntegrityError:
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

            # Distribution des parts aux membres
            try:
                with sqlite3.connect("payouts.db") as conn:
                    c = conn.cursor()
                    for mention in members_list:
                        clean_name = mention.replace("@", "").strip()
                        member = discord.utils.get(interaction.guild.members, name=clean_name)
                        if member:
                            user_id = member.id
                            c.execute('''
                                INSERT INTO user_balances (user_id, balance)
                                VALUES (?, ?)
                                ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?
                            ''', (user_id, per_member, per_member))

                            c.execute('''
                                INSERT INTO payout_users (payout_name, user_id)
                                VALUES (?, ?)
                            ''', (self.payout_name, user_id))
                    conn.commit()
            except Exception as e:
                await interaction.followup.send(f"❌ Erreur lors de la distribution : {e}", ephemeral=True)
                return

            # Message public
            try:
                mentions = ", ".join(members_list)
                await interaction.channel.send(
                    f"💰 **Payout {self.payout_name}** lancé par **{self.caller_name}**\n"
                    f"👥 Membres : {mentions}\n"
                    f"💸 Total : {total:,} • Réparations : {repairs:,}\n"
                    f"🏰 Guilde : {guild_cut:,} • Net : {net:,} • Par membre : {per_member:,}"
                )
            except discord.Forbidden:
                await interaction.followup.send(
                    "⚠️ Je n’ai pas les permissions pour envoyer un message public dans ce salon.",
                    ephemeral=True
                )
                return

            # Confirmation privée
            if interaction.response.is_done():
                await interaction.followup.send("✅ Payout enregistré et distribué avec succès.", ephemeral=True)
            else:
                await interaction.response.send_message("✅ Payout enregistré et distribué avec succès.", ephemeral=True)

        except Exception as e:
            msg = f"❌ Erreur inattendue : {e}"
            if interaction.response.is_done():
                await interaction.followup.send(msg, ephemeral=True)
            else:
                await interaction.response.send_message(msg, ephemeral=True)