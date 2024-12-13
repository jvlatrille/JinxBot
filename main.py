"""
@file main.py
@brief Point d'entrée du bot Discord.
@details Ici, on configure et démarre le bot avec tout ce qu'il faut pour qu'il roule sans accroc (en théorie).
"""

import asyncio
import logging
from discord.ext import commands
from discord import Intents
from config import BOT_TOKEN

"""
@brief Configure les logs pour voir ce que le bot fait.
@details Ça permet d'afficher les infos importantes, les bugs, ou juste savoir quand il se connecte.
"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

"""
@var bot
@param command_prefix Définit le préfixe pour les commandes textuelles (ici, "/").
@param intents Dit au bot ce qu’il a le droit de voir/faire (genre lire les messages, voir les réactions, etc.).
"""
bot = commands.Bot(command_prefix="/", intents=Intents.all())

"""
@var initial_extensions
La liste des "cogs" (modules) que le bot va charger. 
Chaque cog, c’est une partie du bot (par ex. commandes pour salles, admin, etc.).
"""
initial_extensions = [
    "Cogs.salles.Salles",
    "Cogs.ping",
    "Cogs.admin",
]

"""
@brief Charge les modules définis dans `initial_extensions`.
@details Chaque extension est chargée ici et on loggue si ça plante.
"""


async def load_extensions():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logging.info(f"Extension chargée : {extension}")
        except Exception as e:
            logging.error(f"Erreur lors du chargement de {extension} : {e}")


"""
@event on_ready
@brief C'est appelé quand le bot est connecté et prêt.
@details Ici, on affiche un message dans la console pour confirmer, et on synchronise les commandes slash.
"""


@bot.event
async def on_ready():
    logging.info(f"Connecté en tant que {bot.user}")
    try:
        # Synchronisation globale des commandes slash
        synced = await bot.tree.sync()
        if synced:
            logging.info(f"Commandes slash synchronisées : {len(synced)} commandes.\n")
        else:
            logging.info(
                "Commandes slash synchronisées (askip), mais aucune commande n'a été retournée :(\n)"
            )
    except Exception as e:
        logging.error(f"Erreur lors de la synchronisation des commandes >:(\n{e}\n\n")


"""
@brief Point d'entrée asynchrone du bot.
@details Charge les cogs, et démarre le bot avec son token.
"""


async def main():
    async with bot:
        await load_extensions()
        await bot.start(BOT_TOKEN)


"""
@brief Démarre tout.
@details Le code ici lance la boucle asynchrone principale avec `asyncio.run`.
"""
if __name__ == "__main__":
    asyncio.run(main())
