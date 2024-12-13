import asyncio
import logging
from discord.ext import commands
from discord import Intents
from config import BOT_TOKEN

# Configuration de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Préfixe des commandes et intents
bot = commands.Bot(command_prefix="/", intents=Intents.all())

# Liste des extensions à charger
initial_extensions = [
    "Cogs.salles.Salles",
    "Cogs.ping",  # Extension Ping
]

# Chargement des extensions
async def load_extensions():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logging.info(f"Extension chargée : {extension}")
        except Exception as e:
            logging.error(f"Erreur lors du chargement de {extension} : {e}")

@bot.event
async def on_ready():
    logging.info(f"Connecté en tant que {bot.user}")
    try:
        # Synchronisation globale des commandes slash
        synced = await bot.tree.sync()
        if synced:
            logging.info(f"Commandes slash synchronisées : {len(synced)} commandes.")
        else:
            logging.info("Commandes slash synchronisées, mais aucune commande n'a été retournée.")
    except Exception as e:
        logging.error(f"Erreur lors de la synchronisation des commandes : {e}")


# Fonction principale pour lancer le bot
async def main():
    async with bot:
        await load_extensions()  # Charge les extensions
        await bot.start(BOT_TOKEN)  # Démarre le bot

# Exécution principale
if __name__ == "__main__":
    asyncio.run(main())
