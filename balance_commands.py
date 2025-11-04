import sqlite3
from discord.ext import commands
from config import DB_PATH

def setup_balance_commands(bot):

    @bot.command(name="bal")
    async def balance(ctx):
        user_id = ctx.author.id
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT balance FROM user_balances WHERE user_id = ?", (user_id,))
            row = c.fetchone()
        if row:
            await ctx.send(f"💰 Ton solde est de **{row[0]:,}** pièces.")
        else:
            await ctx.send("💸 Aucun solde enregistré pour toi.")

    @bot.command(name="bl")
    async def balance_leaderboard(ctx):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id, balance FROM user_balances ORDER BY balance DESC")
            rows = c.fetchall()

        if not rows:
            await ctx.send("📭 Aucun solde enregistré.")
            return

        message = "**🏆 Classement des balances :**\n"
        for i, (user_id, balance) in enumerate(rows, start=1):
            member = ctx.guild.get_member(user_id)
            name = member.display_name if member else f"<ID:{user_id}>"
            message += f"{i}. **{name}** → {balance:,} pièces\n"

        await ctx.send(message)