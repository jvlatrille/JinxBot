import discord
import logging
from discord import app_commands
from discord.ext import commands, tasks
from discord.app_commands import Choice
from utils.TrouveTaSalle import TrouveTaSalle
from config import ID_PROMOS, timezone, ROLES
import datetime


class Salles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.edt = TrouveTaSalle(ID_PROMOS, refresh_on_init=False)
        self.refresh_edt.start()
        # Liste des professeurs
        self.professeurs = {
            "RICHA": "Jr. Richa",
            "CARPENTIER": "Y. Carpentier",
            "ETCHEVERRY": "P. Etcheverry",
            "MARQUESUZAÀ": "C. Marquesuzaà",
            "BRUYÈRE": "M. Bruyère",
            "MOULIN": "A. Moulin",
            "BORTHWICK": "M. Borthwick",
            "ERRITALI": "M. Erritali",
            "SASSI": "S. Sassi",
            "CHBEIR": "R. Chbeir",
            "NODENOT": "T. Nodenot",
            "YESSOUFOU": "F. YESSOUFOU",
            "BOGGIA": "A. Boggia",
            "CAPLIEZ": "M. Capliez",
            "DEZEQUE": "O. Dezeque",
            "RUSTICI": "C. Rustici",
            "ROOSE": "P. Roose",
            "VOISIN": "S. Voisin (Laplace)",
            "VALLES-PARLANGEAU": "N. Valles-Parlangeau",
            "DAGORRET": "P. Dagorret",
            "BOUDIA": "MA. Boudia",
            "WALTON": "M. Walton",
            "FITON": "JM. Fiton",
            "DOURISBOURE": "Y. Dourisbourne",
            "GASTAMBIDE": "MA. Gastambide",
        }

    async def autocomplete_professeur(
        self, interaction: discord.Interaction, current: str
    ):
        """Méthode pour suggérer des noms de professeurs"""
        # Filtre les noms en fonction de ce qui est tapé
        suggestions = [
            Choice(name=name, value=key)
            for key, name in self.professeurs.items()
            if current.lower() in name.lower()
        ]
        # Limite à 25 résultats (Discord impose cette limite)
        return suggestions[:25]

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

    # COMMANDE INFO_SALLE
    @app_commands.command(
        name="info_salle",
        description="Obtenir des informations sur une salle spécifique.",
    )
    @app_commands.describe(nom_salle="Nom de la salle à vérifier")
    async def info_salle(self, interaction, nom_salle: str):
        """Commande slash pour obtenir les informations d'une salle"""
        salle_info = self.edt.get_info_salle(nom_salle)
        if "error" in salle_info and salle_info["error"] == "NOT FOUND":
            await interaction.response.send_message(
                f"❌ La salle '{nom_salle}' n'existe pas.", ephemeral=True
            )
            return

        # Disponibilité
        disponible = salle_info["now"] is None
        status = "Libre" if disponible else "Occupée"
        status_emoji = "🟢" if disponible else "🔴"

        # Cours actuels
        cours_actuels = (
            f"- {salle_info['now']['name']} "
            f"(de {datetime.datetime.fromtimestamp(salle_info['now']['begin']).strftime('%H:%M')} "
            f"à {datetime.datetime.fromtimestamp(salle_info['now']['end']).strftime('%H:%M')})"
            if salle_info["now"]
            else "Aucun cours en cours actuellement."
        )

        # Créneaux libres
        creneaux_libres = "\n".join(
            f"{datetime.datetime.fromtimestamp(cr[0]).strftime('%H:%M')} à {datetime.datetime.fromtimestamp(cr[1]).strftime('%H:%M')}"
            for cr in salle_info["free"]
        )
        if not creneaux_libres:
            creneaux_libres = "Aucun créneau disponible aujourd'hui."

        # Création de l'embed
        embed = discord.Embed(
            title=f"Informations sur la salle {nom_salle}",
            color=discord.Color.green() if disponible else discord.Color.red(),
            timestamp=datetime.datetime.now(timezone),
        )
        embed.add_field(name="Statut", value=f"{status_emoji} {status}", inline=True)
        embed.add_field(name="Cours en cours", value=cours_actuels, inline=False)
        embed.add_field(name="Disponibilités", value=creneaux_libres, inline=False)
        embed.set_footer(text="Les informations peuvent être incomplètes ou inexactes")

        # Envoi de l'embed
        await interaction.response.send_message(embed=embed)

    # COMMANDE INFO_PROF AVEC AUTOCOMPLÉTION
    @app_commands.command(
        name="info_prof",
        description="Obtenir des informations sur un professeur spécifique.",
    )
    @app_commands.describe(nom_prof="Nom du professeur à vérifier")
    @app_commands.autocomplete(nom_prof=autocomplete_professeur)
    async def info_prof(self, interaction: discord.Interaction, nom_prof: str):
        """Commande slash pour obtenir les informations sur un professeur"""
        # Vérifie si le professeur existe
        if nom_prof.upper() not in self.professeurs:
            await interaction.response.send_message(
                f"❌ Le professeur '{nom_prof}' n'est pas dans la liste.",
                ephemeral=True,
            )
            return

        # Récupération des données
        prof_info = self.edt.get_prof(nom_prof.upper())
        if not prof_info:
            await interaction.response.send_message(
                f"❌ Aucun cours trouvé pour le professeur '{self.professeurs[nom_prof.upper()]}'",
                ephemeral=True,
            )
            return

        # Informations sur le cours actuel
        cours_actuel = (
            f"- **{prof_info['now']['name']}** "
            f"(de {datetime.datetime.fromtimestamp(prof_info['now']['begin']).strftime('%H:%M')} "
            f"à {datetime.datetime.fromtimestamp(prof_info['now']['end']).strftime('%H:%M')}, "
            f"salle : {prof_info['now']['salle']})"
            if prof_info["now"]
            else "Aucun cours en cours actuellement."
        )

        # Liste des cours à venir
        cours = "\n".join(
            f"- **{c['name']}** (de {datetime.datetime.fromtimestamp(c['begin']).strftime('%H:%M')} "
            f"à {datetime.datetime.fromtimestamp(c['end']).strftime('%H:%M')}, salle : {c['salle']})"
            for c in prof_info["cours"]
        )
        if not cours:
            cours = "Aucun cours programmé pour aujourd'hui."

        # Cas particulier pour Chbeir
        if nom_prof.upper() == "CHBEIR":
            cours_actuel = (
                "Actuellement en train d'apprendre le PL/SQL à une table basse."
            )

        # Création de l'embed
        embed = discord.Embed(
            title=f"Informations sur {self.professeurs[nom_prof.upper()]}",
            color=discord.Color.purple(),
            timestamp=datetime.datetime.now().astimezone(timezone),
        )
        embed.add_field(name="Cours en cours", value=cours_actuel, inline=False)
        embed.add_field(name="Cours à venir", value=cours, inline=False)
        embed.set_footer(text="Les informations peuvent être incomplètes ou inexactes")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="salles_libres", description="Retourne les salles libres actuellement, triées par durée de disponibilité.")
    async def salles_libres(self, interaction: discord.Interaction):
        """Commande slash pour obtenir les salles libres"""
        # Récupère les informations sur les salles libres
        info = self.edt.get_salle_libre()

        # Si aucune salle libre
        if not info:
            embed = discord.Embed(
                title="Aucune salle libre actuellement",
                description="Toutes les salles sont occupées ou l'emploi du temps n'est pas encore chargé.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(timezone),
            )
            embed.set_footer(text="Les informations peuvent être incomplètes ou inexactes")
            await interaction.response.send_message(embed=embed)
            return

        # Création de l'embed
        embed = discord.Embed(
            title="Salles libres actuellement",
            description="Triées par durée de disponibilité",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(timezone),
        )

        # Ajout des salles libres avec leurs créneaux
        for salle, creneaux in info.items():
            salle_type = "🖥️ PC" if salle in self.edt.listeSallesPC else "📚 TD"
            debut = datetime.datetime.fromtimestamp(creneaux[0][0]).strftime('%H:%M')
            fin = datetime.datetime.fromtimestamp(creneaux[0][1]).strftime('%H:%M')
            embed.add_field(
                name=f"{salle_type} Salle {salle}",
                value=f"Disponible de **{debut}** à **{fin}**",
                inline=False,
            )

        embed.set_footer(text="Les informations peuvent être incomplètes ou inexactes")
        await interaction.response.send_message(embed=embed)


    @app_commands.command(
        name="emploi_du_temps",
        description="Obtenez votre emploi du temps basé sur vos rôles."
    )
    async def emploi_du_temps(self, interaction: discord.Interaction):
        """Commande slash pour afficher l'emploi du temps de l'utilisateur."""

        # Initialisation des variables
        roles = [role.name for role in interaction.user.roles]
        annee, td, tp = "", "", ""

        # Vérification des rôles
        for role in roles:
            if role in ROLES["Année"]:
                annee = ROLES["Année"][role]
            if role in ROLES["TD"]:
                td = ROLES["TD"][role]
            if role in ROLES["TP"]:
                tp = ROLES["TP"][role]

        # Validation des rôles
        if not annee or not td or not tp:
            await interaction.response.send_message(
                "❌ Vous n'avez pas les rôles nécessaires pour récupérer votre emploi du temps. Vérifiez vos rôles dans le serveur !",
                ephemeral=True,
            )
            return

        # Récupération des cours
        cours = self.edt.get_cours_TD(f"{annee}-{td}-{tp}")
        if not cours["cours"]:
            await interaction.response.send_message(
                "❌ Aucun cours trouvé pour votre TD/TP aujourd'hui.",
                ephemeral=True,
            )
            return

        # Création de l'embed
        embed = discord.Embed(
            title=f"Emploi du temps pour {td}-{tp} (Année {annee})",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(timezone),
        )
        embed.set_footer(text="Les informations peuvent être incomplètes ou inexactes")

        # Ajouter les cours à l'embed
        for cours_info in cours["cours"]:
            heure_debut = datetime.datetime.fromtimestamp(cours_info["begin"]).strftime("%H:%M")
            heure_fin = datetime.datetime.fromtimestamp(cours_info["end"]).strftime("%H:%M")
            embed.add_field(
                name=f"{heure_debut} - {heure_fin}",
                value=f"**{cours_info['name']}** (Salle : {cours_info['salle']})",
                inline=False,
            )

        # Envoi de l'embed
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Salles(bot))
