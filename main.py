import asyncio
import logging
from discord.ext import commands
from discord import Intents
from config import BOT_TOKEN

"""
@file main.py
@brief Point d'entrée du bot Discord.
@details Configure et démarre le bot Discord, charge les extensions et synchronise les commandes slash.
"""

# Configuration de logging pour afficher les informations
"""
@brief Configure les logs pour surveiller l'activité du bot.
@details Affiche les messages d'information, d'erreurs et autres événements importants dans la console.
"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialisation du bot avec un préfixe de commande et des permissions
"""
@var bot
@brief Instance principale du bot Discord.
@param command_prefix Le préfixe des commandes textuelles.
@param intents Les permissions d'intéraction du bot avec Discord.
"""
bot = commands.Bot(command_prefix="/", intents=Intents.all())

# Liste des extensions à charger
"""
@var initial_extensions
@brief Liste des modules (cogs) à charger au démarrage.
@details Chaque module représente une fonctionnalité distincte (ex. gestion des salles, commandes admin).
"""
initial_extensions = [
    "Cogs.salles.Salles",
    "Cogs.ping",
    "Cogs.admin",
]

# Fonction pour charger les extensions
"""
@brief Charge les extensions définies dans `initial_extensions`.
@details Log chaque extension chargée ou les erreurs rencontrées.
"""


async def load_extensions():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logging.info(f"Extension chargée : {extension}")
        except Exception as e:
            logging.error(f"Erreur lors du chargement de {extension} : {e}")


# Événement indiquant que le bot est prêt
"""
@event on_ready
@brief Appelé lorsque le bot est connecté et prêt à l'utilisation.
@details Synchronise les commandes slash et affiche un message dans la console.
"""


@bot.event
async def on_ready():
    logging.info(f"Connecté en tant que {bot.user}")
    try:
        # Synchronisation globale des commandes slash
        synced = await bot.tree.sync()
        if synced:
            logging.info(f"Commandes slash synchronisées : {len(synced)} commandes.")
        else:
            logging.info("Aucune commande synchronisée retournée.")
    except Exception as e:
        logging.error(f"Erreur lors de la synchronisation des commandes : {e}")


# Fonction principale pour lancer le bot
"""
@brief Point d'entrée asynchrone du bot.
@details Charge les extensions et démarre le bot avec son token.
"""


async def main():
    async with bot:
        await load_extensions()
        await bot.start(BOT_TOKEN)


# Démarrage de la boucle principale
"""
@brief Lance la boucle principale asynchrone du bot.
@details Initialise tout en utilisant asyncio.
"""
if __name__ == "__main__":
    asyncio.run(main())
