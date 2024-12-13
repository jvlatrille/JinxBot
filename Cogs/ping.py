import logging
from discord import app_commands
from discord.ext import commands

"""
@file ping.py
@brief Cog pour la commande de test 'ping'.
@details Permet de vérifier la latence du bot Discord.
"""


class Ping(commands.Cog):
    """
    @class Ping
    @brief Cog pour la commande '/ping'.
    @details Fournit une commande pour mesurer la latence du bot.
    """

    def __init__(self, bot):
        """
        @brief Initialise le Cog Ping.
        @param bot Instance du bot Discord.
        """
        self.bot = bot

    @app_commands.command(
        name="ping", description="Retourne le temps de latence du bot."
    )
    async def ping_slash(self, interaction):
        """
        @brief Retourne le temps de latence entre le bot et Discord.
        @param interaction Interaction contenant les informations de la commande.
        @details La latence est calculée en millisecondes et affichée dans la réponse.
        """
        response = f"Pong ! Latence : {round(self.bot.latency * 1000)} ms"
        await interaction.response.send_message(response)
        logging.info(f"{interaction.user} : ping -> {response}")


async def setup(bot):
    """
    @brief Ajoute le Cog Ping au bot.
    @param bot Instance du bot Discord.
    """
    await bot.add_cog(Ping(bot))
