import discord
import sqlite3
from config import DB_PATH

class PayoutModal(discord.ui.Modal, title="Créer un payout"):

    def __init__(self, payout_name: str, caller_name: str):
        super().__init__()
        self.payout_name = payout_name
        self.caller_name = caller_name

        # Champs du formulaire (max 5)
        self.total = discord.ui.TextInput(label="Prix total (€)", placeholder="Ex: 120")
        self.repairs = discord.ui.TextInput(label="Prix réparations (€)", placeholder="Ex: 20")
        self.members = discord.ui.TextInput(label="Membres (séparés par des virgules)", placeholder="Ex: @Nico,@Clara")
        self.guild_member = discord.ui.TextInput(label="Membre guilde ? (oui/non)", placeholder="oui ou non")
        self.guild_percent = discord.ui.TextInput(label="% pour la guilde", placeholder="Ex: 10", required=False)

        # Ajout des champs au modal
        self.add_item(self.total)
        self.add_item(self.repairs)
        self.add_item(self.members)
        self.add_item(self.guild_member)
        self.add_item(self.guild_percent)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            total = float(self.total.value)
            repairs = float(self.repairs.value)
            guild_pct = float(self.guild_percent.value) if self.guild_percent.value else 0
            members_raw = [m.strip().replace("@", "") for m in self.members.value.split(",") if m.strip()]
            member_count = len(members_raw)

            if member_count == 0:
                await interaction.response.send_message("❌ Aucun membre valide renseigné.", ephemeral=True)
                return

            net = total - repairs
            guild_cut = net * (guild_pct / 100)
            to_split = net - guild_cut
            per_member = to_split / member_count

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            # Enregistrement du payout
            c.execute('''
                INSERT INTO payouts (name, caller, total, repairs, guild_percent, guild_cut, net, per_member)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.payout_name,
                self.caller_name,
                total,
                repairs,
                guild_pct,
                guild_cut,
                to_split,
                per_member
            ))

            # Enregistrement des membres
            for name in members_raw:
                user = discord.utils.get(interaction.guild.members, name=name)
                if user:
                    c.execute("INSERT INTO payout_users (payout_name, user_id) VALUES (?, ?)", (self.payout_name, user.id))
                    c.execute('''
                        INSERT INTO user_balances (user_id, balance)
                        VALUES (?, ?)
                        ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?
                    ''', (user.id, per_member, per_member))

            conn.commit()
            conn.close()

            # Confirmation privée
            await interaction.response.send_message(
                f"✅ Payout **{self.payout_name}** créé par **{self.caller_name}**.\n"
                f"Total: {total}€, Réparations: {repairs}€, Net: {net:.2f}€\n"
                f"Guilde ({guild_pct}%): {guild_cut:.2f}€ → À répartir : {to_split:.2f}€\n"
                f"Part par membre ({member_count}) : **{per_member:.2f}€**",
                ephemeral=True
            )

            # Annonce publique
            await interaction.channel.send(
                f"🎉 Le payout **{self.payout_name}** est terminé !\n"
                f"• Caller : {self.caller_name}\n"
                f"• Total : {total}€, Réparations : {repairs}€, Guilde : {guild_cut:.2f}€\n"
                f"• À répartir : {to_split:.2f}€ entre {member_count} membres → **{per_member:.2f}€** chacun\n"
                f"✅ Les balances des membres ont été mises à jour."
            )

        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur : {e}", ephemeral=True)