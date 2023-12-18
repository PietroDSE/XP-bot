import discord
from discord.ext import commands
import asyncio
from xp_tracker_gui import XpTrackerApp, tk

bot = commands.Bot(command_prefix='!')
allowed_channel_name = 'bot-active'
app_instance = None
message_count = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')
    # lógica quando o bot estiver pronto


@bot.event
async def on_message(message):
    global app_instance
    await bot.process_commands(message)
    if not message.author.bot:
        user_id = str(message.author.id)
        # lógica quando uma mensagem for enviada

    if message.channel.name == allowed_channel_name:
        if user_id not in message_count:
            message_count[user_id] = 1
        else:
            message_count[user_id] += 1
        # inicia a contagem de level ao novo usuário

    if message_count[user_id] % 5 == 0:
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
        app_instance.update_gui(200, 2)  # Substitua pelos dados reais

if __name__ == '__main__':
    app_instance = XpTrackerApp(tk.Tk())
    loop = asyncio.get_event_loop()
    loop.create_task(update_gui(app_instance))

bot.run('MTE4NTY4MjY0MDI1MTEyOTkyNw.GN_wWh.xuxLWPNMUwQ_w2uPB7uyV8eOrOyWeJ6YEQ7AwM')
bot.loop.create_task(periodic_task())
