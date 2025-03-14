import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

extensions = ["commands.roll", "commands.music", "commands.merchant", "commands.ficha", "commands.image_gen"]
async def load_extensions():
    for ext in extensions:
        await bot.load_extension(ext)

@bot.event
async def on_ready():
    await load_extensions()
    print(f"Bot {bot.user} está online!")

@bot.command(name="ajuda", help="Lista todos os comandos disponíveis e suas funcionalidades.")
async def ajuda(ctx):
    help_text = "Aqui estão os comandos disponíveis:\n"
    for command in bot.commands:
        help_text += f"/{command.name} - {command.help}\n"
    await ctx.send(help_text)

bot.run(TOKEN)