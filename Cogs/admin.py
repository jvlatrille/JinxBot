import discord
from discord.ext import commands
from discord import app_commands

"""
@file admin.py
@brief Cog pour les commandes d'administration.
@details Contient des commandes permettant de gérer le serveur, telles que la suppression de messages.
"""


class Admin(commands.Cog):
    """
    @class Admin
    @brief Cog pour les commandes d'administration.
    @details Fournit des outils pour gérer efficacement les salons Discord.
    """

    def __init__(self, bot):
        """
        @brief Initialise le Cog Admin.
        @param bot Instance du bot Discord.
        """
        self.bot = bot

    @app_commands.command(
        name="clear",
        description="Supprime un certain nombre de messages dans le salon.",
    )
    @app_commands.describe(nombre="Nombre de messages à supprimer (max. 100)")
    async def clear(self, interaction: discord.Interaction, nombre: int):
        """
        @brief Supprime un nombre défini de messages dans le salon actuel.
        @param interaction Interaction contenant les informations sur la commande slash.
        @param nombre Nombre de messages à supprimer (entre 1 et 100).
        @details Cette commande ne peut être utilisée que par les utilisateurs ayant la permission de gérer les messages.
        @note Le message confirmant la suppression est envoyé de manière éphémère.
        """

        # Vérifie si l'utilisateur a les permissions
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ Vous n'avez pas la permission de gérer les messages.",
                ephemeral=True,
            )
            return

        # Vérifie la limite
        if nombre < 1 or nombre > 100:
            await interaction.response.send_message(
                "❌ Vous devez spécifier un nombre entre 1 et 100.", ephemeral=True
            )
            return

        # Supprime les messages
        deleted = await interaction.channel.purge(limit=nombre)

        # Envoi un message de confirmation
        await interaction.response.send_message(
            f"✅ {len(deleted)} message(s) supprimé(s) par {interaction.user.mention}.",
            ephemeral=True,
        )


async def setup(bot):
    """
    @brief Ajoute le Cog Admin au bot.
    @param bot Instance du bot Discord.
    """
    await bot.add_cog(Admin(bot))
