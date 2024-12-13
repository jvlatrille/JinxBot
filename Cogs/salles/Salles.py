import asyncio
import logging
from discord import app_commands
from discord.ext import commands, tasks
from utils.TrouveTaSalle import TrouveTaSalle
from config import ID_PROMOS, timezone
import datetime


class Salles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.edt = TrouveTaSalle(ID_PROMOS, refresh_on_init=False)
        self.refresh_edt.start()

    def cog_unload(self):
        self.refresh_edt.cancel()

    @tasks.loop(minutes=10)
    async def refresh_edt(self):
        try:
            logging.info("[Salles] Rafraîchissement des emplois du temps")
            result = self.edt.refresh()
            if result == "hour" or result == "weekend":
                logging.info("[Salles] Hors des heures de cours")
            else:
                logging.info("[Salles] Données mises à jour avec succès")
        except Exception as e:
            logging.error(f"[Salles] Erreur lors du rafraîchissement : {e}")

    @commands.command(name="salles_libres")
    async def salles_libres(self, ctx):
        info = self.edt.get_salle_libre()
        if not info:
            await ctx.send("Aucune salle libre actuellement.")
            return

        message = "**Salles libres actuellement :**\n"
        for salle, creneaux in info.items():
            message += f"- {salle} : {creneaux[0][0]} à {creneaux[0][1]}\n"
        await ctx.send(message)

    @app_commands.command(name="info_salle", description="Obtenir des informations sur une salle spécifique.")
    @app_commands.describe(nom_salle="Nom de la salle à vérifier")
    async def info_salle(self, interaction, nom_salle: str):
        """Commande slash pour obtenir les informations d'une salle"""
        salle_info = self.edt.get_info_salle(nom_salle)
        if "error" in salle_info and salle_info["error"] == "NOT FOUND":
            await interaction.response.send_message(f"❌ La salle '{nom_salle}' n'existe pas.", ephemeral=True)
            return

        disponible = "Oui" if salle_info["now"] is None else "Non"
        cours_actuels = (
            f"**Cours actuel :**\n- {salle_info['now']['name']} "
            f"(de {datetime.datetime.fromtimestamp(salle_info['now']['begin']).strftime('%H:%M')} "
            f"à {datetime.datetime.fromtimestamp(salle_info['now']['end']).strftime('%H:%M')})"
            if salle_info["now"]
            else "Aucun cours en cours actuellement."
        )
        creneaux_libres = ", ".join(
            f"{datetime.datetime.fromtimestamp(cr[0]).strftime('%H:%M')} à {datetime.datetime.fromtimestamp(cr[1]).strftime('%H:%M')}"
            for cr in salle_info["free"]
        )
        response = (
            f"**Informations sur la salle '{nom_salle}' :**\n"
            f"- Disponible maintenant : {disponible}\n"
            f"{cours_actuels}\n"
            f"- Créneaux disponibles aujourd'hui : {creneaux_libres}"
        )
        await interaction.response.send_message(response)

async def setup(bot):
    await bot.add_cog(Salles(bot))
