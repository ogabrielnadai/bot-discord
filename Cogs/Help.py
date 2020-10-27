import discord
from discord.ext import commands
import datetime

"""Classe | Comando de Ajuda Personalizado

Contém todos os recursos para uma mensagem de ajuda personalizada, dependendo de certas
valores definidos ao definir um comando em primeiro lugar.
"""
class TheHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        """Ajuda General Bot

        Envie uma lista de ajuda para todos os comandos bot.

        NOTE: Será paginado posteriormente.
        """
        fields = []
        for cog in mapping.keys():
            if cog:
                command_list = await self.filter_commands(mapping[cog], sort = True)
                if len(command_list) > 0:
                    fields.append({
                        "name": cog.qualified_name,
                        "value": f"{cog.description}\nComandos:\n" + ", ".join(f"`{command}`" for command in command_list),
                        "inline": False
                    })
        embed = self.context.bot.embed_util.get_embed(
            title = "Comando Ajuda",
            desc = f"Uma lista de todos os comandos disponíveis classificados por agrupamento. \n Para saber mais sobre comandos específicos, use`{self.clean_prefix}help <command>`",
            fields = fields,
            author = self.context.message.author
        )
        await self.get_destination().send(embed = embed)

    async def send_cog_help(self, cog):
        """Ajuda | COG Especifico

        Envia ajuda para todos os comandos contidos em um cog, por
        nome da engrenagem.
        """
        embed = self.context.bot.embed_util.get_embed(
            title = f"{cog.qualified_name} Help",
            desc = f"{cog.description}\nPara saber mais sobre comandos específicos, use `{self.clean_prefix}help <comando>`",
            author = self.context.message.author,
            fields = [{
                "name": "Commands",
                "value": "\n".join("`{1.qualified_name}`".format(command) for command in cog.walk_commands() if not command.hidden),
                "inline": False
            }]
        )
        await self.get_destination().send(embed = embed)

    async def send_group_help(self, group):
        """Ajuda Comandos agrupados

        Envia uma mensagem de ajuda para todos os comandos agrupados em um comando pai.
        """
        command_list = group.walk_commands()
        command_activation = []
        command_example = []
        for command in command_list:
            if "`" + command.qualified_name + " " + command.signature + "` - {}".format(command.help) not in command_activation and not command.hidden:
                command_activation.append("`" + command.qualified_name + " " + command.signature + "` - {}".format(command.help))
                if command.brief:
                    command_example.append("`" + self.clean_prefix + command.qualified_name + " " + command.brief + "`")
                else:
                    command_example.append("`" + self.clean_prefix + command.qualified_name + "`")

        fields = []
        if group.aliases:
            fields.append({
                "name": "Outros",
                "value": ", ".join('`{}`'.format(alias) for alias in group.aliases),
                "inline": False
            })
        fields.append({
            "name": "Comandos",
            "value": "\n".join(command_activation),
            "inline": False
        })
        fields.append({
            "name": "Examplo",
            "value": "\n".join(command_example),
            "inline": False
        })

        embed = self.context.bot.embed_util.get_embed(
            title = f"'{group.qualified_name.capitalize()}' Help",
            desc = f"{group.help}\n\nFPara obter mais informações sobre cada comando, use `{self.clean_prefix}help [command]`.",
            fields = fields,
            author = self.context.message.author
        )
        await self.get_destination().send(embed = embed)

    async def send_command_help(self, command):
        """Ajuda Comando Específico

        Envie ajuda para um único comando específico.
        """
        fields = []
        if command.aliases:
            fields.append({
                "name": "Outros",
                "value": ", ".join('`{}`'.format(alias) for alias in command.aliases),
                "inline": False
            })
        fields.append({
            "name": "Uso",
            "value": "`" + self.clean_prefix + command.qualified_name + " " + command.signature + "`",
            "inline": False
        })
        if command.brief:
            fields.append({
                "name": "Exemplo",
                "value": "`" + self.clean_prefix + command.qualified_name + " " + command.brief + "`",
                "inline": False
            })
        else:
            fields.append({
                "name": "Examplo",
                "value": "`" + self.clean_prefix + command.qualified_name + "`",
                "inline": False
            })
        embed = self.context.bot.embed_util.get_embed(
            title = f"'{command.name.capitalize()}' Help",
            desc = f"{command.help}",
            fields = fields,
            author = self.context.message.author
        )
        await self.get_destination().send(embed = embed)
"""Cog | Class Loader

Carrega a classe de comando de ajuda personalizada acima.
"""
class LoadHelp(commands.Cog, name = "Help"):
    """
    Lista todos os comandos disponíveis, classificados pelo Cog em que estão.
    """
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = TheHelpCommand()
        bot.help_command.cog = self
        print(f"{bot.OK} {bot.TIMELOG()} Cog Help Carregado")

def setup(bot):
    """Configuração

    A função chamada por Discord.py ao adicionar outro arquivo em um projeto de vários arquivos.
    """
    bot.add_cog(LoadHelp(bot))
