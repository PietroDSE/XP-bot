import discord 
from discord.ext import commands
import pyrebase
import os
#importação do banco de dados
MForXP = 5
#5 mensagens = 5 XP (obs: só será creditado o XP após 5 mensagens)
firebase_config = {
    "apiKey": "AIzaSyB4ISp7E-mIG0S3r5T5xwfmTWGB1-puqDQ",
    "authDomain": "bot-xp-7cc5d.firebaseapp.com",
    "databaseURL": "https://bot-xp-7cc5d.firebaseio.com",
    "projectId": "bot-xp-7cc5d",
    "storageBucket": "bot-xp-7cc5d.appspot.com",
    "messagingSenderId": "345854080880",
    "appId": "1:345854080880:web:790ce7ecac71fcf11001b5",
    "measurementId": "G-YPL4JMN8HS"
}
#configuração da database

firebase = bot.initialize_app(firebase_config)
db = firebase.database()
#inicialização da database

bot = commands.Bot(command_prefix ='!')
#adiciona o prefixo do comando

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')
#evento quando o bot está pronto

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_id =str(message.author.id)
#evento quando uma mensagem é enviada
    
xp = db.child('users').child(user_id).child('xp').get().val() or 0
xp += 5
#adiciona 5 pontos de XP a cada 5 mensagens

db.child('users').child('users_id').update({'xp': xp})
#atualiza o XP no banco de dados

check_level(user_id, xp)
#verifica e atualiza o nível de XP

await bot.process_commands(message)
#processa os comandos

@bot.command(name='level')
async def level(ctx):
    user_id = str(ctx.author.id)
    xp = db.child('Users').child(user_id).child('xp').get().val() or 0
    level = db.child('Users').child(user_id).child('level').get().val() or 0
    await ctx.send(f'{ctx.author.mention}), seu nível é {level}\n e você tem {xp} pontos de XP')
#comando de verificação de nível
    
def check_level(user_id, xp):
    #...
    #lógica de verificação de nível
bot.run('')