import asyncio
import logging
from discord.ext import commands
from discord import Intents
from config import BOT_TOKEN

# Configuration de logging pour afficher les informations
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


bot = commands.Bot(command_prefix="/", intents=Intents.all())

# Liste des extensions à charger
initial_extensions = [
    "Cogs.salles.Salles",
    "Cogs.ping",
    "Cogs.admin",
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
            logging.info(f"Commandes slash synchronisées : {len(synced)} commandes.\n")
        else:
            logging.info("Commandes slash synchronisées (askip), mais aucune commande n'a été retournée :(\n)")
    except Exception as e:
        logging.error(f"Erreur lors de la synchronisation des commandes >:(\n{e}\n\n")


# Fonction principale pour lancer le bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(BOT_TOKEN)

# Exécution principale
if __name__ == "__main__":
    asyncio.run(main())
