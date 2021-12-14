import discord
from discord.ext import commands
from urllib import parse, request
import json
from discord.utils import get
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN_ID = os.environ.get("TOKEN_ID")
TOKEN = os.environ.get("TOKEN")
UPDATE_TIME = int(os.environ.get("UPDATE_TIME"))
DECIMALS = int(os.environ.get("DECIMALS"))

def data_crypto():#consultamos los datos de la cryptomoneda
    response = request.urlopen('https://api.coingecko.com/api/v3/coins/' + TOKEN_ID).read()
    return json.loads(response.decode('utf-8'))




bot = commands.Bot(command_prefix='!', description="This is a helper bot")

    

# Events
@bot.event
async def on_ready():
        print('My Bot is ready')
    
        #actualizamos el avatar del bot una sola vez
        try:
            req = request.Request(data_crypto()['image']['large'], headers={'User-Agent': 'Mozilla/5.0'})
            img = request.urlopen(req).read()
            await bot.user.edit( avatar=img)
        finally:
            while not bot.is_closed():
                try:
                    crypto = data_crypto()#obtenemos los datos de la consulta

                    for guild in bot.guilds: #obtenemos los datos de la "guild" para cambiar el role y el apodo(nickname)
                        
                        #obtenemos los roles para cambiar el color del apodo
                        role_low = get(guild.roles, name='low')
                        role_high = get(guild.roles, name='high')

                        #if los roles no existe los crea
                        if(role_low == None):
                            role_low = await guild.create_role(name="low", permissions=discord.Permissions(), colour=discord.Colour.red())
                        if(role_high == None):
                            role_high = await guild.create_role(name="high", permissions=discord.Permissions(), colour=discord.Colour.green())
                        
                        # almacenara la flecha que llevara el nombre        
                        type_arrow = '' 
                        #if el porcentaje bajo el role asignado será "low" de lo contrario será "high", con sus recpectiva flecha
                        if(crypto['market_data']['price_change_percentage_24h'] < 0):
                            await guild.me.add_roles(role_low)
                            await guild.me.remove_roles(role_high)
                            type_arrow = '↘️'
                        else:
                            await guild.me.add_roles(role_high)
                            await guild.me.remove_roles(role_low)
                            type_arrow = '↗️'
                        # print('{:f}'.format(round(crypto['market_data']['current_price']['usd'], DECIMALS)))
                        # print(round(crypto['market_data']['price_change_24h'], DECIMALS))
                        # print("{:f}({:f}%)".format(
                        #     round(crypto['market_data']['price_change_24h'], DECIMALS), 
                        #     round(crypto['market_data']['price_change_percentage_24h'], DECIMALS)
                        # ))
                        # print(round(crypto['market_data']['price_change_24h'], DECIMALS))
                        await guild.me.edit(nick=crypto['symbol'].upper() + f' {type_arrow} ' + str(round(crypto['market_data']['current_price']['usd'], DECIMALS)))
                        
                    #cambia la "presence" asignandolo un nombre del cambio del precio en 24h y el cambio del pocentaje en 24h
                    await bot.change_presence(activity=discord.Game(
                        name = 
                            str(round(crypto['market_data']['price_change_24h'], DECIMALS)) + 
                            f"({round(crypto['market_data']['price_change_percentage_24h'], DECIMALS)}%)"
                    ))

                    #tiempo de espera para volver a actualizar
                except BaseException as err:
                    print(err)

                await asyncio.sleep(UPDATE_TIME)
                    
bot.run(TOKEN)