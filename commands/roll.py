import random
import re
from discord.ext import commands

class DiceRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rolar", help="Rola um dado. Exemplo: /rolar 2d8+3d12+2")
    async def roll_dice(self, ctx, roll: str):
        pattern = r"(\d+)d(\d+)"
        matches = re.findall(pattern, roll)
        modifiers = re.findall(r"[+-]\d+", roll)

        if not matches:
            await ctx.send("Formato inválido! Use: `/rolar 2d6+3`")
            return

        total = 0
        details = []

        for i, match in enumerate(matches):
            qtd, faces = int(match[0]), int(match[1])
            rolls = [random.randint(1, faces) for _ in range(qtd)]
            mod = int(modifiers[i]) if i < len(modifiers) else 0
            subtotal = sum(rolls) + mod
            details.append(f"{rolls} + {mod} = {subtotal}")
            total += subtotal

        await ctx.reply(f"🎲 Rolagem: {'; '.join(details)}\n**Total: {total}**")

async def setup(bot):
    await bot.add_cog(DiceRoll(bot))