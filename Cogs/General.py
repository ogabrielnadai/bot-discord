import discord
from discord.ext import commands
import datetime
from math import trunc
import sys

"""Cog Comandos Gerais

Este Cog contém uma lista de comandos que quase todos os programas
deve utilizar.

NOTE: Todos os comandos são restritos ao uso do servidor apenas por padrão,
remova a linha `@ commands.guild_only ()` antes de qualquer comando que
também deve poder ser usado em um DM.
"""
class General(commands.Cog, name = "General"):
    """
    Um conjunto geral de comandos.
    """
    def __init__(self, bot):
        self.bot = bot
        print(f"{bot.OK} {bot.TIMELOG()} Cog General Carregado")

    @commands.guild_only()
    @commands.command(name = "prefix", help = "Altera o prefixo do comando para o bot.", brief = "?")
    async def prefix(self, ctx, prefix: str):
        if self.bot.delete_commands:
            await ctx.message.delete()

        old = self.bot.prefix
        self.bot.config['Prefix'] = prefix
        with open('./Config.yml', 'w') as file:
            self.bot.yaml.dump(self.bot.config, file)

        self.bot.prefix = prefix
        if self.bot.show_game_status:
            game = discord.Game(name = self.bot.game_to_show.format(prefix = self.bot.prefix))
            await self.bot.change_presence(activity = game)

        embed = self.bot.embed_util.get_embed(
            title = "Prefix Atualizado",
            desc = f"Novo Prefix: `{self.bot.prefix}`",
            fields = [
                {"name": "New", "value": f"{self.bot.prefix}command", "inline": True},
                {"name": "Old", "value": f"{old}command", "inline": True},
            ],
            author = ctx.author
        )
        await ctx.send(embed = embed)
        embed = self.bot.embed_util.update_embed(embed, ts = True, author = ctx.author)
        await self.bot.log_channel.send(embed = embed)

    @commands.guild_only()
    @commands.command(name = "restart", help = "Reinicia o bot.", brief = "")
    async def restart(self, ctx):
        """Comando Reinicia o bot.

        NOTE: Envia uma mensagem para o canal de log, adiciona uma reação à mensagem e, em seguida,
        tenta reinicar o bot

        Um script Lote ou Shell (dependendo do sistema operacional) será então
        reative o bot, o que permite que o bot receba atualizações de arquivos em tempo real.
        """
        embed = self.bot.embed_util.get_embed(
            title = self.bot.restarting_message.format(username = self.bot.user.name),
            ts = True,
            author = ctx.author
        )
        await self.bot.log_channel.send(embed = embed)

        await ctx.message.add_reaction('✅')
        await self.bot.close()
    
    @commands.guild_only()
    @commands.command(name = "stopbot", help = "Desliga o bot.", brief = "")
    async def stopbot(self, ctx):
        """Comando para desligar o BOT.

        NOTE: Envia uma mensagem para o canal de log, adiciona uma reação à mensagem e, em seguida,
        tenta desconectar-se do Discord.

        Um script Lote ou Shell (dependendo do sistema operacional) será então
        reative o bot, o que permite que o bot receba atualizações de arquivos em tempo real.
        """
        embed = self.bot.embed_util.get_embed(
            title = self.bot.stop_message.format(username = self.bot.user.name),
            ts = True,
            author = ctx.author
        )
        await self.bot.log_channel.send(embed = embed)
        
        await ctx.message.add_reaction('✅')
        await self.bot.close()
        await self.bot.logout()
        sys.exit(2)

    @commands.guild_only()
    @commands.command(name='uptime', help = 'Retorna a quantidade de tempo que o bot esteve online.')
    async def uptime(self, ctx):
        """Comando Get Bot Uptime

        Como o nome indica ... isso retorna a quantidade de tempo que o
        bot está online, já que o valor `bot.start_time`
        foi definido em `main.py` na função` on_ready`.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        seconds = trunc((datetime.datetime.now(datetime.timezone.utc) - self.bot.start_time).total_seconds())
        hours = trunc(seconds / 3600)
        seconds = trunc(seconds - (hours * 3600))
        minutes = trunc(seconds / 60)
        seconds = trunc(seconds - (minutes * 60))

        embed = self.bot.embed_util.get_embed(
            title = f":alarm_clock: {self.bot.user.name} Time Online",
            desc = f"{hours} Horas\n{minutes} Minutos\n{seconds} Segundos",
            ts = True,
            author = ctx.author
        )
        await ctx.send(embed = embed)

    @commands.guild_only()
    @commands.command(name='ping', aliases=['pong'], help = 'Obtém a latência atual do bot.')
    async def ping(self, ctx):
        """Comando Obter Bot Ping

        Retorna dois valores, o ping do bot Discord na API,
        e o tempo de ping que leva quando a mensagem original é enviada
        para quando o bot postar sua resposta com êxito.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        embed = self.bot.embed_util.get_embed(
            title = ":ping_pong: Pong!",
            desc = "Calculando tempo de Ping...",
            author = ctx.author
        )
        m = await ctx.send(embed = embed)

        embed = self.bot.embed_util.update_embed(
            embed = embed,
            desc = "A latência da mensagem é {} ms\nA latência da API de discórdia é {} ms".format(
                trunc((m.created_at - ctx.message.created_at).total_seconds() * 1000),
                trunc(self.bot.latency * 1000)
            )
        )
        await m.edit(embed = embed)

    @commands.guild_only()
    @commands.command(name='invite', help = 'Retorna o link de convite do servidor.', brief = "")
    async def invite(self, ctx):
        """Comando Obter convite para servidor

        Retorna um link de convite estático definido no arquivo Config.yml.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        embed = self.bot.embed_util.get_embed(
            title = "Convidar link",
            desc = f"{self.bot.invite_link}",
            author = ctx.author
        )
        await ctx.send(embed = embed)

    @commands.guild_only()
    @commands.command(name='clear', help = 'Limpa o chat do canal atual.', brief = "[Quantidade de Mensagens]")
    async def clear(self, ctx, amount=5, channel: discord.TextChannel=None):
        """Comando para limpar o canal atual

        Por padrão ele deleta 5 linhas, passar parametro para mais linhas.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        count = 0
        channel = channel or ctx.channel

        # Contando a quantidade de mensagens do channel onde comando foi dado (O channel pode ser passado como parametro)
        async for channel in channel.history(limit=None):
            count += 1

        # Verificando se quantidade de mensagens existentes no canal é menor que a quantidade de mensagens que foram pedidas para apagar
        if count < amount:
            amount = count
        else:
            pass

        # Apaga as mensagens(Parametro limit é a quantidade de mensagens apagadas)
        await ctx.channel.purge(limit=amount)

        embed = self.bot.embed_util.get_embed(
            title = "Chat apagado.",
            desc = f"Quantidade de linhas apagadas: {amount} Linhas.",
            author = ctx.author
        )
        await ctx.send(embed = embed)
        embed = self.bot.embed_util.update_embed(
            embed = embed,
            author = ctx.author,
            ts = True
        )
        await self.bot.log_channel.send(embed = embed)

        # Apagando própria mensagem do bot
        await ctx.channel.purge(limit=1)
def setup(bot):
    """Configuração

    A função chamada por Discord.py ao adicionar outro arquivo em um projeto de vários arquivos.
    """
    bot.add_cog(General(bot))
