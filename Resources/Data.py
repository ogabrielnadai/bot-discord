"""Resource | Gerenciador de dados

Esta classe gerencia todo o carregamento e
salvamento da configuração, permissões e dados.
"""
import json
import os
from discord import Color
from colorama import Fore
import datetime

class DataManager():
    def __init__(self, bot):
        self.bot = bot

    def load_config(self):
        """Setup | Bot Config

        Carregando variáveis ​​de configuração em atributos de bot.

        Veja 'Config.yml' para detalhes sobre cada configuração.
        """
        with open("./Config.yml", 'r') as file:
            config = self.bot.yaml.load(file)

        # Salve os arquivos de configuração no bot.
        self.bot.config = config

        # Configurações principais
        self.bot.TOKEN               = config['Token Env Var']
        self.bot.prefix              = config['Prefix']
        self.bot.online_message      = config['Online Message']
        self.bot.restarting_message  = config['Restarting Message']
        self.bot.stop_message        = config['Stop Message']
        self.bot.data_file           = os.path.abspath(config['Data File'])
        self.bot.show_game_status    = config['Game Status']['Active']
        self.bot.game_to_show        = config['Game Status']['Game']
        self.bot.log_channel_id      = config['Log Channel']
        self.bot.broken_user_id      = config['Broken User ID']
        self.bot.invite_link         = config['Server Invite']

        # Opções de incorporação
        self.bot.embed_color = Color.from_rgb(
            config['Embed Settings']['Color']['r'],
            config['Embed Settings']['Color']['g'],
            config['Embed Settings']['Color']['b']
        )
        self.bot.footer =              config['Embed Settings']['Footer']['Text']
        self.bot.footer_image =        config['Embed Settings']['Footer']['Icon URL']
        self.bot.delete_commands =     config['Embed Settings']['Delete Commands']
        self.bot.show_command_author = config['Embed Settings']['Show Author']
        self.bot.embed_ts =            lambda: datetime.datetime.now(datetime.timezone.utc)

        # Variáveis ​​de log
        self.bot.OK = f"{Fore.GREEN}[OK]{Fore.RESET}  "
        self.bot.WARN = f"{Fore.YELLOW}[WARN]{Fore.RESET}"
        self.bot.ERR = f"{Fore.RED}[ERR]{Fore.RESET} "
        self.bot.TIMELOG = lambda: datetime.datetime.now().strftime('[%m/%d/%Y | %I:%M:%S %p]')

    def load_permissions(self):
        """Setup | Permissões de comando

        Carregando variáveis ​​de permissão nos atributos do bot.

        Consulte 'Permissions.yml' para obter detalhes sobre cada configuração.
        """
        bot_permissions = {}
        with open("./Permissions.yml", 'r') as file:
            permissions = self.bot.yaml.load(file)
            # A entrada de permissão bruta é formatada para ter IDs de função no local.
            roles = dict(permissions['Roles'])
            for key in permissions.keys():
                if not key in (None, 'Roles'):
                    bot_permissions[key] = []
                    for permission in permissions[key]:
                        bot_permissions[key].append(permission.format(**roles))

        self.bot.permissions = permissions

    def save_data(self):
        """Data | Salvar

        Abra o arquivo de dados e salve os dados do bot nele.

        Substitui os dados anteriores no arquivo.
        """
        with open(self.bot.data_file, 'w+', encoding = "utf-8") as save_file:
            try:
                save_file.write(json.dumps(self.bot.data, indent = 2))
            except Exception as e:
                print('Não foi possível salvar os dados: ' + str(e))

    def load_data(self):
        """Data | Carregar

        Verifique se o arquivo de dados existe, se existir, carregue-o, se não, crie-o.

        Se o arquivo de dados existir, mas não possuir dados, forneça um novo objeto de dados vazio.
        """
        if os.path.exists(self.bot.data_file):
            with open(self.bot.data_file, 'r', encoding = "utf-8") as file:
                content = file.read()
                if len(content) == 0:
                    self.bot.data = {}
                    self.save_data()
                else:
                    self.bot.data = json.loads(content)
        else:
            self.bot.data = {}
            self.save_data()
