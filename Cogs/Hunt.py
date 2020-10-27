import discord
from discord.ext import commands
import datetime

"""Cog | Template

Contém comando de criação da sala de HUNT e a exclusão da mesma quando o usuário
autor da sala sair

NOTE: Todos os comandos são restritos ao uso do servidor apenas por padrão,
remova a linha `@ commands.guild_only ()` antes de qualquer comando que
também deve poder ser usado em um DM.
"""
class Hunt(commands.Cog, name = "Hunt"):
    """
    Comandos usando para criar sala de hunt
    """
    def __init__(self, bot):
        self.bot = bot
        print(f"{bot.OK} {bot.TIMELOG()} Cog Hunt Carregado")

    @commands.guild_only()
    @commands.command(name = "salahunt", aliases=['sala hunt'], help = "Comandos para criar uma nova sala de HUNT (LEMBRE-SE DE ESTAR EM UM CANA DE VOZ).", brief = "Nâo há parametros")
    async def sample(self, ctx):
        """Command | salahunt

        Cria uma nova sala de voz contendo o nome HUNT--NOME_DO_AUTOR_DO_COMANDO e
        move o autor do comando para essa sala.
        """
        if self.bot.delete_commands:
            await ctx.message.delete()

        guild = ctx.guild
        id_category_channel = None
        try:
            for channel in guild.channels:
                if channel.name == 'TIBIA-HUNTS':
                    id_category_channel = self.bot.get_channel(channel.id)

            if id_category_channel == None:
                embed = self.bot.embed_util.get_embed(
                    title = f"Você precisa ter uma categoria chamada TIBIA-HUNTS no seu Discord",
                    desc = f"O nome deve ser exatamente TIBIA-HUNTS"
                )

                await ctx.send(embed = embed)

            else:
                name_author_channel = split_member_name(str(ctx.author))
                name_hunt_channel = 'HUNT--{}'.format(name_author_channel)

                try:
                    await guild.create_voice_channel(name_hunt_channel, category=id_category_channel)
                    for channel in guild.channels:
                        if channel.name == name_hunt_channel:
                            object_hunt_channel = self.bot.get_channel(channel.id)
                    await ctx.author.move_to(object_hunt_channel, reason=None)

                    embed = self.bot.embed_util.get_embed(
                        title = "{} foi movido para o canal {}".format(name_author_channel, name_hunt_channel),
                        desc = f"Lembre-se que o canal é excluido quando o dono da sala sair"
                    )

                    await ctx.send(embed = embed)

                except:
                    embed = self.bot.embed_util.get_embed(
                        title ='Você não está conectado a um canal de voz!',
                        desc = f"Por favor conecte-se a um canal de voz"
                    )

                    await ctx.send(embed = embed)
                    await object_hunt_channel.delete()
        except:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listener | Sample

        Este é um modelo para um ouvinte de mensagem padrão.
        """
        if not message.author.bot:
            pass
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Listener | on_voice_state_update

        Este é um modelo para um ouvinte do estado de voice channels para 
        deletar o canal HUNT-- quando usuário é disconnectado.
        """
        if 'HUNT--' not in str(after.channel):
            if 'HUNT--' in str(before.channel):
                channel_before_name = str(before.channel)
                hunt_prefix, nome_dono_da_sala = channel_before_name.split('--')
                hunt_prefix == hunt_prefix
                nome_author_state = split_member_name(str(member))
                if nome_dono_da_sala == nome_author_state:
                    await before.channel.delete()

def setup(bot):
    """Setup

    A função chamada por Discord.py ao adicionar outro arquivo em um projeto de vários arquivos.
    """
    bot.add_cog(Hunt(bot))

def split_member_name(name_member):
    """split_member_name

    Quebra o nome do usuário a partir do "#" retornando somente o nome
    """
    name_of_author_return, hashtag_atrelada = name_member.split('#')
    hashtag_atrelada = hashtag_atrelada
    return name_of_author_return
