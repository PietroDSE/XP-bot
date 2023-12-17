import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, db
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Inicializa o Firebase
cred = credentials.Certificate("Usuários/davill08/Downloads/bot-xp-7cc5d-firebase-adminsdk-htkae-b802b0aa1c")
firebase_admin.initialize_app(cred, {"databaseURL": "https://bot-xp-7cc5d.firebaseio.com"})
ref = db.reference("users")

# Configuração do bot
bot = commands.Bot(command_prefix="!")

# Função para obter o hash do usuário
def get_user_hash(user_id):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(user_id.encode('utf-8'))
    return digest.finalize()

# Função para calcular o nível com base na pontuação
def calculate_level(xp):
    # Lógica de cálculo do nível (personalize conforme necessário)
    return xp // 100  # Exemplo simples: 100 pontos por nível

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_id = str(message.author.id)
    user_hash = get_user_hash(user_id)

    # Lógica para obter e atualizar XP com user_hash
    user_ref = ref.child(user_hash.hex())
    xp = user_ref.child("xp").get() or 0
    xp += 5
    user_ref.update({"xp": xp})

    # Lógica para calcular o nível
    level = calculate_level(xp)

    # Restante da lógica com user_hash
    # ...

    await bot.process_commands(message)

@bot.command(name="level")
async def level(ctx):
    user_id = str(ctx.author.id)
    user_hash = get_user_hash(user_id)

    # Lógica para obter nível e XP com user_hash
    user_ref = ref.child(user_hash.hex())
    xp = user_ref.child("xp").get() or 0
    level = calculate_level(xp)

    await ctx.send(f"{ctx.author.mention}, seu nível é {level} e você tem {xp} pontos de XP")

# Substitua 'YOUR_BOT_TOKEN' pelo seu token real
bot.run("YOUR_BOT_TOKEN")
