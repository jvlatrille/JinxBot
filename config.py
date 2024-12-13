# config.py

import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import confidentiel

# Chargement des variables d'environnement
load_dotenv()

# Token du bot
BOT_TOKEN = confidentiel.TOKENBOTPROMO

# Variables liées au semestre
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

# Rôles Discord
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

# Configuration du fuseau horaire
timezone = "Europe/Paris"
