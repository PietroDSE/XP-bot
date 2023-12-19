import discord
import tkinter as tk
from discord.ext import commands
import asyncio
from discord import Intents
from config import SharedConfig
from xp_tracker_gui import XpTrackerApp
import logging
from math import pow


# Configuração do logger raiz
logging.basicConfig(level=logging.DEBUG)

# Criando loggers específicos para diferentes partes do código
logger_main = logging.getLogger('main')
logger_xp = logging.getLogger('xp')

# Configuração para exibir logs no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Configurar para o nível desejado
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger_main.addHandler(console_handler)
logger_xp.addHandler(console_handler)

intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
shared_config = SharedConfig()


@bot.event
async def on_ready():
    try:
        loop.create_task(update_gui(shared_config))
    except Exception as e:
        logger_main.error(f'Erro inesperado em on_ready: {e}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if not message.author.bot:
        await process_user_message(message)


async def update_level(user_id, xp, message):
    level = calculate_level(shared_config, user_id)
    app_instance.update_gui(xp, level)
    await message.channel.send(f'Parabéns <@{user_id}>! Você tá no level {level}!')


async def process_user_message(message):
    user_id = str(message.author.id)

    # Lógica quando uma mensagem for enviada
    shared_config.db_cursor.execute("INSERT INTO messages (guild_id, channel_id, author_id, content) VALUES (?, ?, ?, ?)",
                                    (message.guild.id, message.channel.id, message.author.id, message.content))
    shared_config.db_connection.commit()

    if user_id in shared_config.message_count:
        if message.channel.name == shared_config.allowed_channel_name:
            await handle_allowed_channel_message(user_id, message)

        if shared_config.message_count[user_id] % 5 == 0:
            xp_gain = 5
            xp = 5
        else:
            await handle_non_5th_message(user_id, message)


async def handle_allowed_channel_message(user_id, message):
    shared_config.message_count[user_id] += 1
    # Inicia a contagem de level ao novo usuário

    xp = 5
    await update_level(user_id, xp, message)


async def handle_non_5th_message(user_id, message):
    shared_config.message_count[user_id] += 1

    level = calculate_level(shared_config, user_id)

    if level > shared_config.user_levels.get(user_id, 1):
        shared_config.user_levels[user_id] = level
        await app_instance.notify_level_up(user_id, level)

    xp = 5
    app_instance.update_gui(xp, level)
    await message.channel.send(f'Parabéns <@{user_id}>! Você tá no Level {level}!')


async def update_gui_on_ready(shared_config, app_instance):
    while True:
        await asyncio.sleep(10)
        for user_id, level in shared_config.user_levels.items():
            await app_instance.notify_level_up(user_id, level)


def calculate_level(shared_config, user_id):
    try:
        xp_to_next_level = shared_config.xp_to_next_level
        xp = shared_config.user_xp.get(user_id, 0)

        ratio = xp / xp_to_next_level

        if 0 <= ratio <= 1:
            level = 1 + int(pow(ratio, 1 / 1.2))
            remaining_xp = xp_to_next_level - \
                int(xp_to_next_level * pow(1.2, level))
        else:
            level = 1
            remaining_xp = 0

        shared_config.user_xp[user_id] = remaining_xp
        shared_config.xp_to_next_level = int(xp_to_next_level * 1.2)

        return level
    except ValueError as e:
        logger_xp.error(f'Erro de valor ao calcular o level: {e}')
        return 1


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command(name='MyXP')
async def my_xp(ctx):
    # Lista de IDs de canais permitidos
    allowed_channels = [1186457318850838539]
    if ctx.channel.id not in allowed_channels:
        await ctx.send('Canal errado! Vai lá em #comandos!')
        return

    user_id = str(ctx.author.id)
    xp = shared_config.user_xp.get(user_id, 0)
    level = calculate_level(shared_config, user_id)

    app_instance.start_progress_bar()
    # inicia a barra de tarefas

    await asyncio.sleep(5)
    # simula um processamento demorado(5seg)

    app_instance.stop_progress_bar()
    # para a barra de progresso

    app_instance.update_progress_bar()
    # atualiza a barra de progresso

    await ctx.send(f'Você tem {xp} de XP e está no Level {level}! Continue assim!')
    # mensagem executando o comando !MyXP


async def periodic_task():
    while True:
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Game(name="I'm active!"))


async def update_gui(bot):
    try:
        while True:
            await asyncio.sleep(10)
            app_instance.update_gui(200, 2)
    except AttributeError as e:
        logger_main.error(f'Erro de atributo ao atualizar GUI: {e}')


if __name__ == '__main__':
        
    shared_config.db_cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                    (guild_id INTEGER, channel_id INTEGER, author_id INTEGER, content TEXT)''')
    shared_config.db_connection.commit()
    master = tk.Tk()
    app_instance = XpTrackerApp(master, shared_config)
    try:
        loop = asyncio.get_event_loop()
        tasks = [
            bot.start('MTE4NTY4MjY0MDI1MTEyOTkyNw.GDzv9k.Do4kgvMHp7PhBOeuOKt8uxyNjklHWvjq87nlxs'),
            update_gui(bot),
            periodic_task(),
            update_gui_on_ready(shared_config, app_instance),

        ]
        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
    


