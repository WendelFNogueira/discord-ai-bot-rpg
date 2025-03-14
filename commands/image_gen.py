import discord
import torch
import os
import threading
import re
from discord.ext import commands
from diffusers import StableDiffusionPipeline

# Nome do modelo e pasta de armazenamento
MODEL_NAME = "runwayml/stable-diffusion-v1-5"
MODEL_PATH = "./stable-diffusion-model"

class ImageGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.livro_t20 = self.carregar_livro()
        self.pipe = None
        threading.Thread(target=self.load_model, daemon=True).start()  # Carrega o modelo em outra thread

    @staticmethod
    def carregar_livro():
        with open("data/infobook/tormenta_20_collab.txt", "r", encoding="utf-8") as f:
            return f.read()

    def find_context(self, prompt):
        pattern = re.compile(rf"{re.escape(prompt)}.*?(?=\n\n|$)", re.IGNORECASE | re.DOTALL)
        matches = pattern.findall(self.livro_t20)
        return "\n\n".join(matches[:5]) if matches else "Contexto não encontrado no livro."

    def load_model(self):
        """Carrega o modelo, baixando se necessário."""
        print("🔄 Verificando modelo de IA...")
        if not os.path.exists(MODEL_PATH):
            print("⬇️ Modelo não encontrado. Baixando...")
            pipe = StableDiffusionPipeline.from_pretrained(MODEL_NAME)
            pipe.save_pretrained(MODEL_PATH)
            print("✅ Modelo baixado e salvo localmente.")
        else:
            print("✅ Modelo já está disponível localmente.")

        # Carrega o modelo salvo
        self.pipe = StableDiffusionPipeline.from_pretrained(MODEL_PATH)
        self.pipe.to("cuda" if torch.cuda.is_available() else "cpu")  # Usa GPU se disponível
        print("🚀 Modelo carregado e pronto para uso!")

    async def generate_image(self, prompt):
        if self.pipe is None:
            print("⚠️ Modelo ainda não carregado. Aguardando...")
            return None

        context = self.find_context(prompt)
        full_prompt = f"Arte inspirada no livro de RPG de mesa Tormenta20: {prompt}\n\nContexto do livro:\n{context}"

        try:
            image = self.pipe(full_prompt).images[0]  # Gera a imagem
            image_path = f"generated_images/{prompt[:50].replace(' ', '_')}.png"
            image.save(image_path)
            return image_path
        except Exception as e:
            print(f"❌ Erro ao gerar imagem: {e}")
            return None

    @commands.command(name="gerar_imagem", help="Gera uma imagem baseada em uma descrição. Exemplo: /gerar_imagem <descrição>")
    async def gerar_imagem(self, ctx, *, descricao: str):
        prompt = descricao
        async with ctx.typing():
            image_path = await self.generate_image(prompt)
            if image_path:
                await ctx.reply(file=discord.File(image_path))
            else:
                await ctx.send("Erro ao gerar imagem. O modelo pode ainda estar carregando.")

async def setup(bot):
    await bot.add_cog(ImageGen(bot))