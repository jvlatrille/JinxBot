import logging  # Import du module logging
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commande slash
    @app_commands.command(name="ping", description="Retourne le temps de latence du bot.")
    async def ping_slash(self, interaction):
        response = f"Pong ! Latence : {round(self.bot.latency * 1000)} ms"
        await interaction.response.send_message(response)
        logging.info(f"{interaction.user} : ping -> {response}")

async def setup(bot):
    await bot.add_cog(Ping(bot))
