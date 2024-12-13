import os
from dotenv import load_dotenv
import sys
import confidentiel
import pytz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"""
@file config.py
@brief Fichier de configuration pour le bot Discord.
@details Stocke les informations essentielles comme les tokens, les promotions, les rôles, et les fuseaux horaires.
"""

# Chargement des variables d'environnement
"""
@brief Charge les variables d'environnement depuis un fichier `.env`.
@details Permet de garder des informations sensibles hors du code visible.
"""
load_dotenv()

# Token du bot
"""
@var BOT_TOKEN
@brief Token secret pour authentifier le bot Discord.
@details Importé depuis le module confidentiel pour garantir la sécurité.
"""
BOT_TOKEN = confidentiel.TOKENBOTPROMO

# Configuration des promotions
"""
@var SEMESTRE
@brief Définit le semestre en cours.
@details Valeur par défaut : "1" si non spécifié dans les variables d'environnement.

@var ID_PROMOS
@brief Associe chaque groupe TD/TP à un identifiant unique.
@details Utilisé pour récupérer les emplois du temps des différents groupes.
"""
SEMESTRE = os.getenv("SEMESTER", "1")
ID_PROMOS = {
    "1-TD1-TP1": "368",
    "1-TD1-TP2": "369",
    "1-TD2-TP3": "371",
    "1-TD2-TP4": "372",
    "1-TD3-TP5": "373",
    "2-TD1-TP1": "394",
    "2-TD1-TP2": "395",
    "2-TD2-TP1": "397",
    "2-TD2-TP2": "398",
}

# Configuration des rôles Discord
"""
@var ROLES
@brief Structure hiérarchique des rôles sur le serveur Discord.
@details Contient les rôles par TD, TP et année, avec leurs identifiants.
"""
ROLES = {
    "TD": {
        "959814970336510022": "TD1",
        "959815001642790942": "TD2",
        "959815034530324590": "TD3",
    },
    "TP": {
        "959815069665996800": "TP1",
        "959815092390752256": "TP2",
        "959815110157828147": "TP3",
        "959815124938534962": "TP4",
        "959815142038700052": "TP5",
    },
    "Année": {
        "959809924798496799": "1",
        "959809978875650108": "2",
        "959810006537093210": "3",
    },
}

# Fuseau horaire
"""
@var timezone
@brief Définit le fuseau horaire utilisé par le bot.
@details Par défaut : Europe/Paris.
"""
timezone = pytz.timezone("Europe/Paris")
