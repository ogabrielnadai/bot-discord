import discord
from discord.ext import commands
import datetime

"""Cog | Manipulador de Erros

Essa engrenagem lida com todos os erros do bot, impedindo
o tempo de execução de travar ou forçar a saída do bot.

NOTE: Todos os comandos são restritos ao uso do servidor apenas por padrão,
remova a linha `@ commands.guild_only ()` antes de qualquer comando que
também deve poder ser usado em um DM.
"""
class Errors(commands.Cog, name = "Error Handling"):
    """
    Comandos relacionados ao tratamento de erros de bot.
    """
    def __init__(self, bot):
        self.bot = bot
        print(f"{bot.OK} {bot.TIMELOG()} Cog Erros Carregado")

    @commands.guild_only()
    @commands.command(name = "broken", aliases = ['borked'], help = "Usado para relatar quando o bot parou de funcionar", brief = "")
    async def err_report(self, ctx):
        """Comando Denunciar bot quebrado

        Este comando é usado para relatar quando o bot está quebrado ou parou de funcionar,
        imprime algumas informações úteis no console e tenta
        sibile o proprietário do bot.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        user = self.bot.get_user(self.bot.broken_user_id)
        embed = self.bot.embed_util.get_embed(
            title = "Eu estou Quebrado",
            desc = f"Venha me Concertar {user.mention}!",
            author = ctx.author
        )
        await ctx.send(content = user.mention, embed = embed)

        self.print_log(type = self.bot.WARN, message = "Received 'broken' Command", ctx = ctx)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Ouvinte | Manipulador de erro de comando

        Capture erros específicos do comando e retorne a resposta ao usuário
        com base em erro.

        Se o erro não estiver na lista de erros tratados diretamente,
        responda com o erro de comando e envie um log do erro para
        o canal de log.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        if isinstance(error, commands.CommandNotFound):
            self.print_log(type = self.bot.WARN, message = "Comando não encontrado", ctx = ctx)
            embed = self.bot.embed_util.get_embed(
                title = "Comando não encontrado",
                author = ctx.author
            )
            await ctx.send(embed = embed)
            embed = self.bot.embed_util.update_embed(
                embed = embed,
                author = ctx.author,
                ts = True
            )
            await self.bot.log_channel.send(embed = embed)

        elif isinstance(error, commands.BadArgument) and "not found" in str(error):
            self.print_log(type = self.bot.ERR, message = f"{str(error).split(' ')[0]} Não encontrado", ctx = ctx, err = error)
            embed = self.bot.embed_util.get_embed(
                title =  f"{str(error).split(' ')[0]} Não encontrado",
                author = ctx.author,
                fields = [{
                    "name": "Received",
                    "value": "`" + str(error).split('\"')[1] + "`",
                    "inline": False
                }]
            )
            await ctx.send(embed = embed)
            embed = self.bot.embed_util.update_embed(
                embed = embed,
                author = ctx.author,
                ts = True
            )
            await self.bot.log_channel.send(embed = embed)

        elif isinstance(error, commands.CheckFailure):
            self.print_log(
                type = self.bot.WARN,
                message = "Usuário tentou usar o comando sem permissão",
                ctx = ctx
            )

            embed = self.bot.embed_util.get_embed(
                title = "Permissão Negada",
                desc = f"Lamento {ctx.author.name}.",
                author = ctx.author
            )
            await ctx.send(embed = embed)
            embed = self.bot.embed_util.update_embed(
                embed = embed,
                author = ctx.author,
                ts = True
            )
            await self.bot.log_channel.send(embed = embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            error = str(error).split(" ")
            error[0] = '`' + error[0] + '`'
            error = " ".join(error)

            self.print_log(type = self.bot.ERR, message = "Parâmetro obrigatório ausente", err = error, ctx = ctx)

            embed = self.bot.embed_util.get_embed(
                title = "Parâmetro obrigatório ausente",
                desc = error.split(' ')[0],
                author = ctx.author
            )
            await ctx.send(embed = embed)
            embed = self.bot.embed_util.update_embed(
                embed = embed,
                author = ctx.author,
                ts = True
            )
            await self.bot.log_channel.send(embed = embed)

        else:
            embed = self.bot.embed_util.get_embed(
                title = "Comando Falhou",
                desc = str(error),
                author = ctx.author
            )
            await ctx.send(embed = embed)
            embed = self.bot.embed_util.update_embed(
                embed = embed,
                author = ctx.author,
                ts = True
            )
            await self.bot.log_channel.send(embed = embed)

            await self.err_report(ctx)
            self.print_log(type = self.bot.ERR, message = error)

    @commands.Cog.listener()
    async def on_error(self, error):
        """Ouvinte | Manipulador de erro global

        O manipulador generalizado de todos os erros que ocorrem no bot,
        impedindo a suspensão do tempo de execução se algo der errado.
        """
        self.print_log(type = self.bot.ERR, message = error)

    def print_log(self, type, message, err = None, ctx = None):
        print(f"{type} {self.bot.TIMELOG()} {message}:")
        if err:
            print(f"{' ' * 35} Error: {err}")
        if ctx:
            failed_com = ctx.message.content.split(' ')
            if len(failed_com) > 1:
                print(f"{' ' * 35} Comando: {failed_com[0]} | Args: {' '.join(failed_com[1:])}")
            else:
                print(f"{' ' * 35} Comando: {failed_com[0]}")
            print(f"{' ' * 35} Autor: {ctx.author} | ID: {ctx.author.id}")
            print(f"{' ' * 35} Channel: {ctx.channel} | ID: {ctx.channel.id}")

def setup(bot):
    """Configuração

    A função chamada por Discord.py ao adicionar outro arquivo em um projeto de vários arquivos.
    """
    bot.add_cog(Errors(bot))
