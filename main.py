import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")

@bot.command(name="criarcanal")
async def criar_canais(ctx):
    if ctx.author.guild_permissions.administrator:
        config = { # <- Configurações de como será a criação dos canais(categoria, canais, permissão, texto ou voz, etc...)
            "category_name": "Casino",
            "permis_id": [],
            "canais": [
                {"type": "text", "title": "apresentação"},
                {"type": "text", "title": "membros"},
                {"type": "text", "title": "avisos"},
                {"type": "text", "title": "tabelas-preço"},
                {"type": "text", "title": "registro-vendas"},
                {"type": "text", "title": "baú"},
                {"type": "voice", "title": "radio¹"},
                {"type": "voice", "title": "radio²"},
            ],
        }

        category_name = config["category_name"]
        permis_ids = config["permis_id"]

        category = await ctx.guild.create_category(category_name)

        for canal_config in config["canais"]:
            canal_type = canal_config["type"]
            canal_title = canal_config["title"]

            if canal_type == "text":
                channel = await category.create_text_channel(canal_title)
            elif canal_type == "voice":
                channel = await category.create_voice_channel(canal_title)
            else:
                await ctx.send(f"Tipo de canal inválido: {canal_type}")
                continue

            overwrites = {}
            for permis_id in permis_ids:
                user = ctx.guild.get_member(permis_id)
                if user:
                    overwrites[user] = discord.PermissionOverwrite(read_messages=True)

            await channel.edit(overwrites=overwrites)

        await ctx.send(f"Canais criados com sucesso na categoria '{category_name}'")
    else:
        await ctx.send("Você não tem permissão para executar este comando.")


bot.run("TOKEN_DO_BOT_AQUI")
