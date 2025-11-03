import sqlite3
from discord.ext import commands
from config import DB_PATH

def setup_admin_commands(bot):

    @bot.command()
    @commands.has_role("Admin")
    async def validate_payout(ctx, name: str):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE payouts SET validated = 1 WHERE name = ?", (name,))
        if c.rowcount:
            await ctx.send(f"✅ Payout **{name}** validé.")
        else:
            await ctx.send("❌ Payout introuvable ou déjà validé.")
        conn.commit()
        conn.close()

    @bot.command()
    @commands.has_role("Admin")
    async def delete_payout(ctx, name: str):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM payout_users WHERE payout_name = ?", (name,))
        c.execute("DELETE FROM payouts WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        await ctx.send(f"🗑️ Payout **{name}** supprimé.")

    @bot.command()
    @commands.has_role("Admin")
    async def list_payouts(ctx):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name, total, repairs FROM payouts WHERE validated = 0")
        rows = c.fetchall()
        conn.close()
        if not rows:
            await ctx.send("📭 Aucun payout en attente.")
            return
        message = "**📦 Payouts en attente :**\n"
        for name, total, repairs in rows:
            message += f"• {name} → Total: {total}€, Réparations: {repairs}€\n"
        await ctx.send(message)