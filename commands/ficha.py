from discord.ext import commands
import aiohttp
from config import OLLAMA_SERVER_URL

class Ficha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.livro_t20 = self.carregar_livro()

    def carregar_livro(self):
        with open("data/infobook/tormenta_20_collab.txt", "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    async def query_ollama(prompt):
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "top_p": 0.9}
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(OLLAMA_SERVER_URL, json=payload) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("response", "❌ Erro ao acessar o modelo no Ollama.")
        except aiohttp.ClientError as e:
            print(f"Erro ao conectar ao Ollama: {e}")
            return "❌ Erro ao acessar o modelo no Ollama."

    @commands.command(name="preencher_ficha", help="Preenche a ficha do personagem. Exemplo: /preencher_ficha <dados>")
    async def preencher_ficha(self, ctx, *, ficha: str):
        prompt = (
            f"Baseado no livro Tormenta20:\n{self.livro_t20[:2000]}\n"
            f"Como preencher a ficha para '{ficha}'?"
        )

        async with ctx.typing():
            resposta = await self.query_ollama(prompt)
            await ctx.send(f"📜 Guia de Ficha: {resposta}")

async def setup(bot):
    await bot.add_cog(Ficha(bot))