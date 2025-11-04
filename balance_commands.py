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
    async def balance_short(ctx):
        await balance(ctx)