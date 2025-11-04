import sqlite3
from discord.ext import commands
from config import DB_PATH

def setup_text_commands(bot):

    # 💰 Commande !bal : voir sa propre balance
    @bot.command()
    async def bal(ctx):
        user_id = ctx.author.id
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT balance FROM user_balances WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()

        total = row[0] if row else 0
        await ctx.send(f"💰 {ctx.author.name}, ta balance totale est de **{total:.2f}€**.")

    # 📊 Commande !bl : voir toutes les balances triées + stats globales
    @bot.command()
    async def bl(ctx):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user_id, balance FROM user_balances ORDER BY balance DESC")
        rows = c.fetchall()
        conn.close()

        if not rows:
            await ctx.send("📭 Aucun utilisateur n'a de balance.")
            return

        total_circulation = sum(balance for _, balance in rows)
        user_count = len(rows)

        message = "**📊 Balances des utilisateurs (triées) :**\n"
        for user_id, balance in rows:
            user = await bot.fetch_user(user_id)
            message += f"• {user.name} → {balance:.2f}€\n"

        message += f"\n**💰 Argent total en circulation :** {total_circulation:.2f}€\n"
        message += f"**👥 Nombre total d’utilisateurs :** {user_count}"

        await ctx.send(message)