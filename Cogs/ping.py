import logging  # Import du module logging
from discord import app_commands
from discord.ext import commands

"""
    @brief Cog pour la commande de test 'ping'.
    @details Permet de vérifier la latence du bot.
    """


class Ping(commands.Cog):
    """
    @brief Initialise la classe Ping.
    @param bot Instance du bot Discord.
    """

    def __init__(self, bot):
        self.bot = bot

    """
        @brief Retourne le temps de latence entre le bot et le serveur Discord.
        @param interaction Interaction contenant les informations sur la commande slash.
        @details La latence est affichée en millisecondes dans la réponse et enregistrée dans les logs.
        """

    @app_commands.command(
        name="ping", description="Retourne le temps de latence du bot."
    )
    async def ping_slash(self, interaction):
        response = f"Pong ! Latence : {round(self.bot.latency * 1000)} ms"
        await interaction.response.send_message(response)
        logging.info(f"{interaction.user} : ping -> {response}")


"""
    @brief Ajoute le Cog Ping au bot.
    @param bot Instance du bot Discord.
    """


async def setup(bot):
    await bot.add_cog(Ping(bot))
