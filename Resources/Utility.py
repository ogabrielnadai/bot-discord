"""Resource | Funções de utilidade

Este arquivo hospeda classes / funções que são usadas regularmente em todo
o programa. Mais detalhes fornecidos para cada um.
"""
import discord
import datetime

class EmbedUtil:
    def __init__(self, bot):
        self.embed_color = bot.embed_color
        self.footer = bot.footer
        self.footer_image = bot.footer_image
        self.timestamp = bot.embed_ts
        self.show_author = bot.show_command_author

    def get_embed(self, title = None, desc = None, fields = None, ts = False, author = None, thumbnail = None, image = None):
        """Function | Criar mensagem incorporada

        Esta função lê as configurações de incorporação padrão do bot
        atributos e cria uma mensagem incorporada às especificações
        da entrada.
        """
        embed = discord.Embed(
            title = title,
            description = desc,
            color = self.embed_color
        )
        embed.set_footer(
            text = self.footer,
            icon_url = self.footer_image
        )
        if ts:
            embed.timestamp = self.timestamp()
        if self.show_author == True and author:
            embed.set_author(
                name = author.name,
                icon_url = author.avatar_url
            )
        if fields:
            for field in fields:
                embed.add_field(
                    name = field['name'],
                    value = field['value'],
                    inline = field['inline']
                )
        if thumbnail:
            embed.set_thumbnail(
                url = thumbnail
            )
        if image:
            embed.set_image(
                url = image
            )
        return embed

    def update_embed(self, embed, title = None, desc = None, ts = False, author = None, thumbnail = None, image = None):
        """Function | Modificar mensagem incorporada

        Esta função recebe uma mensagem incorporada e a modifica
        com base em entradas.
        """
        if title:
            embed.title = title
        if desc:
            embed.description = desc
        if ts == True:
            embed.timestamp = self.timestamp()
        if author:
            embed.set_author(
                name = author.name,
                icon_url = author.avatar_url
            )
        if thumbnail:
            embed.set_thumbnail(
                url = thumbnail
            )
        if image:
            embed.set_image(
                url = image
            )
        return embed
