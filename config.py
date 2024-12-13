"""
@file config.py
@brief Fichier de configuration pour le bot.
@details Ici, on stocke toutes les configs importantes : token, promos, rôles, et fuseau horaire.
"""

import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import confidentiel
import pytz


"""
@brief Charge les variables d'environnement depuis un fichier `.env`.
@details Utile pour garder des infos sensibles (comme les tokens) hors du code visible( c'est pas ce que j'utilise, mais c'est une bonne pratique).
"""
load_dotenv()


"""
@var BOT_TOKEN
Le token secret du bot, importé depuis le module confidentiel (fichier local non partagé).
"""
BOT_TOKEN = confidentiel.TOKENBOTPROMO


"""
@var SEMESTRE
Le semestre en cours. Défini dans les variables d'environnement ou "1" par défaut.
@var ID_PROMOS
Dictionnaire associant chaque groupe TD/TP à un ID unique pour l'emploi du temps.
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


"""
@var ROLES
Dictionnaire des rôles Discord associés aux TD, TP, et années. Permet de savoir qui appartient à quel groupe.
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


"""
@var timezone
Fuseau horaire utilisé pour tout ce qui est lié au temps (horaires, dates, etc.).
"""
timezone = pytz.timezone("Europe/Paris")
