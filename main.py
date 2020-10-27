'''
Importações da Biblioteca Python
Bibliotecas para, bem ... Dicord.
Data e hora ... eu realmente preciso explicar?
Ruamel.Yaml para permitir que os comentários permaneçam nos arquivos YAML ao lê-los / gravá-los.
Sistema operacional para sistema de arquivos e coisas variáveis ​​de ambiente.
Resources.Data para gerenciamento repetitivo de arquivos de dados, encontrado em ./Resources/Data.py
Colorama para log colorido.
'''

import discord
from discord.ext import commands
import datetime
from ruamel.yaml import YAML
import os
from Resources.Data import DataManager
from Resources.Utility import EmbedUtil
from colorama import init, Fore
init()

# load Arquivo de configuração e permissões.
yaml = YAML()

def get_prefix(bot, message):
    """Prefixo | Gerenciador de prefixo dinâmico

    Permite alterar dinamicamente o prefixo lendo de
    configura ativamente.

    O comando 'prefix' pode atualizar o prefixo bot dessa maneira.
    """
    return bot.prefix

# Crie a instância 'bot', usando a função acima para obter o prefixo.
bot = commands.Bot(command_prefix=get_prefix, description="LizardBot", case_insensitive = True)

# Remova o comando help para deixar espaço para implementar um personalizado.
bot.remove_command('help')

# Salve a ferramenta yaml no bot.
bot.yaml = yaml

"""Instalação | Bot Config

Carregando variáveis ​​de configuração e permissão nos atributos do bot.

Consulte 'Config.yml' e 'Permissions.yml' para obter detalhes sobre cada configuração.
"""
bot.data_manager = DataManager(bot)
bot.data_manager.load_config()
bot.data_manager.load_permissions()
bot.data_manager.load_data()
bot.embed_util = EmbedUtil(bot)

# Lista de arquivos de extensão a serem carregados.
extensions = [
    'Cogs.Errors',
    'Cogs.General',
    'Cogs.Help',
    'Cogs.Hunt'
]

# Carregue os arquivos de extensão listados acima.
for extension in extensions:
    bot.load_extension(extension)

print(f"{bot.OK} {bot.TIMELOG()} Connectando ao Discord") 

@bot.event
async def on_ready():
    """Ouvinte | Conexão Discord

    Disparado quando o bot se conecta com sucesso ao Discord.

    Define a configuração inicial restante para o bot e carrega todas as engrenagens.
    """

    # Obtenha o objeto do canal de log primeiro, isso permite erros compartimentados.
    bot.log_channel = bot.get_channel(bot.log_channel_id) 

    print(f"{bot.OK} {bot.TIMELOG()} Logado como {bot.user} e conectado ao Discord! (BOT ID: {bot.user.id})") 

    # Defina o status de reprodução do bot para o que está definido na configuração.
    if bot.show_game_status:    
        game = discord.Game(name = bot.game_to_show.format(prefix = bot.prefix)) 
        await bot.change_presence(activity = game)

    # Crie modelo de mensagem online.
    embed = bot.embed_util.get_embed(
        title = bot.online_message.format(username = bot.user.name), 
        ts = True
    )
    # Defina o objeto do canal de log como uma variável bot para uso posterior.
    try:
        bot.log_channel = bot.get_channel(bot.log_channel_id) 
        await bot.log_channel.send(embed = embed)
    except:
        print(f"{bot.ERR} {bot.TIMELOG()} Problema ao encontrar ID do canal de log do discord") 

    # Defina a hora de início do bot para uso no comando uptime
    bot.start_time = bot.embed_ts() 

@bot.check
async def command_permissions(ctx):
    """Verifique | Gerente de permissão global

    Isso está anexado a todos os comandos.

    Quando um comando é usado, esta função usa as permissões importadas
    em Permissions.yml para verificar se um usuário é / não é permitido
    para usar um comando
    """
    # Os administradores sempre têm permissão para usar o comando.
    if ctx.author.guild_permissions.administrator:
        return True
    else:
        # Localizando o esquema de nome de permissão de um comando.
        name = ctx.command.name
        if ctx.command.parent:
            command = ctx.command
            parent_exists = True
            while parent_exists == True:
                name = ctx.command.parent.name + '-' + name
                command = ctx.command.parent
                if not command.parent:
                    parent_exists = False

        """Verificando permissões de comando

        Para cada ID de função listada para um comando, verifique se o usuário tem esse ID de função.

        Se o fizerem, permita o uso do comando; caso contrário, continue com a verificação da próxima função na lista.
        """
        if name in ctx.bot.permissions.keys():
            for permission in ctx.bot.permissions[name]:
                try:
                    role = ctx.guild.get_role(int(permission))
                    if role in ctx.author.roles:
                        return True
                except Exception as e:
                    print(e)
            return False
        else:
            return True

try:
    bot.run(bot.TOKEN, bot = True, reconnect = True)
    bot.data_manager.save_data()
except discord.LoginFailure:
    print(f"{bot.ERR} {bot.TIMELOG()} Variável TOKEN inválida: {bot.TOKEN}")
    input("Pressione Enter para continuar.")
