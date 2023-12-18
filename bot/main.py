# bot_file.py
import discord
from discord.ext import commands
import asyncio
from discord import Intents
from config import SharedConfig
from xp_tracker_gui import XpTrackerApp

intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

shared_config = SharedConfig()

app_instance = XpTrackerApp(shared_config)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

    loop = asyncio.get_event_loop()
    loop.create_task(update_gui(app_instance))

@bot.event
async def on_message(message):
    global shared_config
    await bot.process_commands(message)
    if not message.author.bot:
        user_id = str(message.author.id)
        # lógica quando uma mensagem for enviada

        # Armazena a mensagem no banco de dados
        shared_config.db_cursor.execute("INSERT INTO messages (guild_id, channel_id, author_id, content) VALUES (?, ?, ?, ?)",
                (message.guild.id, message.channel.id, message.author.id, message.content))
        shared_config.db_connection.commit()

    if message.channel.name == shared_config.allowed_channel_name:
        if user_id not in shared_config.message_count:
            shared_config.message_count[user_id] = 1
        else:
            shared_config.message_count[user_id] += 1
        # inicia a contagem de level ao novo usuário

    if shared_config.message_count[user_id] % 5 == 0:
        xp_gain = 5
        # método de obtenção de xp
        xp = 200
        level = 2
        app_instance.update_gui(xp, level)
        # atualização do GUI

@bot.command(name='level')
async def level(ctx):
    # Lógica do comando !level aqui
    await ctx.send('Comando !level executado.')

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')
    #comando para manter o bot ativo

async def periodic_task():
    while True:
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="I'm active!"))

async def update_gui(app):
    # Lógica para obter dados do bot Discord e atualizar a GUI
    while True:
        # Exemplo: Atualizar a GUI a cada 10 segundos
        await asyncio.sleep(10)
        app.update_gui(200, 2)  # Substitua pelos dados reais

if __name__ == '__main__':
    # Criação da tabela de mensagens no banco de dados
    shared_config.db_cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                (guild_id INTEGER, channel_id INTEGER, author_id INTEGER, content TEXT)''')
    shared_config.db_connection.commit()

    loop = asyncio.get_event_loop()
    loop.create_task(periodic_task())
    loop.create_task(update_gui())
    bot.run('MTE4NTY4MjY0MDI1MTEyOTkyNw.G143v-.azWC67h_CE4_-8PgYNjPUepR2r0w3KZe88tXrcx')
