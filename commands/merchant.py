import aiohttp
import re
from discord.ext import commands
from config import OLLAMA_SERVER_URL

class Merchant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.book_context = self.carregar_livro()
        self.transactions = {"sold": [], "bought": []}

    @staticmethod
    def carregar_livro():
        with open("data/infobook/base-dados-mercador.txt", "r", encoding="utf-8") as f:
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

    def find_item_context(self, item):
        pattern = re.compile(rf"{re.escape(item)}.*?(?=\n\n|$)", re.IGNORECASE | re.DOTALL)
        matches = pattern.findall(self.book_context)
        return "\n\n".join(matches[:5]) if matches else "Item não encontrado no livro."

    @commands.command(name="comprar", help="Compra um item da loja. Exemplo: /comprar <item>")
    async def comprar_item(self, ctx, *, item: str):
        item_context = self.find_item_context(item)
        print("Item context:", item_context)

        prompt = (
            f"Você é um mercador medieval experiente no mundo de Tormenta20, sempre pronto para negociar armas, itens e acessórios com aventureiros. "
            f"Seu objetivo é vender os itens disponíveis, usando um tom amigável e persuasivo. "
            f"Adapte sua fala como um verdadeiro comerciante medieval, usando expressões típicas da época para tornar a interação mais imersiva."
            f"\n\nUm cliente chamado {ctx.author.display_name} acaba de entrar na sua loja e deseja comprar um item chamado '{item}'."
            f" Aqui estão as informações extraídas do livro Tormenta20 para referência:\n\n{item_context}\n\n"
            f"Apresente-se como mercador e receba o cliente com entusiasmo. "
            f"Descreva o item de maneira envolvente, destacando seus benefícios e funcionalidades, como um vendedor habilidoso faria. "
            f"Se o item for uma arma, enfatize seu poder em combate; se for uma armadura, ressalte sua resistência; se for um item mágico, fale sobre seus encantamentos."
            f"\n\nApós apresentar o item, mencione o preço de forma persuasiva e incentive o cliente a comprá-lo, "
            f"oferecendo até mesmo um pequeno desconto, um brinde ou uma história interessante sobre a peça."
            f" Pergunte se ele deseja algo mais e incentive-o a olhar outros produtos da loja."
            f"\n\nUse um tom envolvente e bem-humorado, mantendo a interação natural e divertida. "
            f"Evite soar robótico e adapte a fala ao contexto de um mercador medieval."
            f"\n\nLembre-se: Sua resposta deve ser curta e direta, não excedendo 2000 caracteres."
        )

        async with ctx.typing():
            response = await self.query_ollama(prompt)
            print("response:", response)
            await ctx.reply(f"🛒 Mercador: {response}", mention_author=True)
            self.transactions["sold"].append(item)

    @commands.command(name="vender", help="Vende um item da loja. Exemplo: /vender <item>")
    async def vender_item(self, ctx, *, item: str):
        item_context = self.find_item_context(item)
        print("Item context:", item_context)

        prompt = (
            f"Você é um mercador medieval experiente no mundo de Tormenta20, sempre pronto para negociar armas, itens e acessórios com aventureiros. "
            f"Seu objetivo é avaliar e comprar itens oferecidos pelos aventureiros, usando um tom amigável e persuasivo. "
            f"Adapte sua fala como um verdadeiro comerciante medieval, usando expressões típicas da época para tornar a interação mais imersiva."
            f"\n\nUm cliente chamado {ctx.author.display_name} acaba de entrar na sua loja e deseja vender um item chamado '{item}'."
            f" Aqui estão as informações extraídas do livro Tormenta20 para referência:\n\n{item_context}\n\n"
            f"Apresente-se como mercador e receba o cliente com entusiasmo. "
            f"Avalie o item de maneira detalhada, destacando seus benefícios e funcionalidades, como um avaliador habilidoso faria. "
            f"Se o item for uma arma, enfatize seu poder em combate; se for uma armadura, ressalte sua resistência; se for um item mágico, fale sobre seus encantamentos."
            f"\n\nApós avaliar o item, mencione o preço de forma persuasiva e ofereça uma quantia justa para comprá-lo, "
            f"oferecendo até mesmo um pequeno bônus ou uma história interessante sobre a peça."
            f" Pergunte se ele deseja vender mais algum item e incentive-o a olhar outros produtos da loja."
            f"\n\nUse um tom envolvente e bem-humorado, mantendo a interação natural e divertida. "
            f"Evite soar robótico e adapte a fala ao contexto de um mercador medieval."
            f"\n\nLembre-se: Sua resposta deve ser curta e direta, não excedendo 2000 caracteres."
        )

        async with ctx.typing():
            response = await self.query_ollama(prompt)
            print("response:", response)
            await ctx.reply(f"🛒 Mercador: {response}", mention_author=True)
            self.transactions["bought"].append(item)

async def setup(bot):
    await bot.add_cog(Merchant(bot))