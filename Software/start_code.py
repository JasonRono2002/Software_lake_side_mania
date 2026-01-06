# import modulen
from pathlib import Path
import json
import pprint
from tkinter import ON
from database_wrapper import Database


# initialisatie

# parameters voor connectie met de database
db = Database(
    host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark"
)


# main

# Haal de eigenschappen op van een personeelslid
# altijd verbinding openen om query's uit te voeren
db.connect()

# pas deze query aan om het juiste personeelslid te selecteren
select_query = "SELECT * FROM personeelslid WHERE id = 1"
personeelslid = db.execute_query(select_query)

# altijd verbinding sluiten met de database als je klaar bent
db.close()

pprint.pp(
    personeelslid
)  # print de resultaten van de query op een overzichtelijke manier
print(personeelslid[0]["naam"])  # voorbeeld van hoe je bij een eigenschap komt


# Haal alle onderhoudstaken op
# altijd verbinding openen om query's uit te voeren
db.connect()

# pas deze query aan en voeg queries toe om de juiste onderhoudstaken op te halen
select_query = "SELECT * FROM onderhoudstaak"
onderhoudstaken = db.execute_query(select_query)
select_query_staff = (
    "SELECT * FROM personeelslid"  # om alle personeelsleden op te halen
)
personeelsLeden = db.execute_query(select_query_staff)

select_query_staffTask = (
    "SELECT * FROM `onderhoudstaak` "
    "INNER JOIN personeelslid "
    "ON onderhoudstaak.`beroepstype` = personeelslid.`beroepstype`"
    f"WHERE personeelslid.`id` = {personeelslid[0]['id']}"
)  # Om alle personeelsleden met hun taken op te halen
personeelsLidTaken = db.execute_query(
    select_query_staffTask
)  # Om alle personeelsleden met hun taken op te halen

select_query_staffAge = "SELECT leeftijd FROM personeelslid"
personeelsLedenLeeftijd = db.execute_query(select_query_staffAge)

# Bepaal de maximale fysieke belasting op basis van de leeftijd
if personeelsLedenLeeftijd[0]["leeftijd"] <= 24:
    maximale_fysieke_belasting = 25
elif 25 <= personeelsLedenLeeftijd[0]["leeftijd"] <= 50:
    maximale_fysieke_belasting = 40
else:
    maximale_fysieke_belasting = 20


# altijd verbinding sluiten met de database als je klaar bent
db.close()

pprint.pp(
    onderhoudstaken
)  # print de resultaten van de query op een overzichtelijke manier

pprint.pp(
    personeelsLeden
)  # print de resultaten van de query op een overzichtelijke manier


# verzamel alle benodigde gegevens in een dictionary
dagtakenlijst = {
    "personeelsgegevens": {
        "naam": personeelslid[0][
            "naam"
        ],  # voorbeeld van hoe je bij een eigenschap komt
        "werktijd": personeelslid[0]["werktijd"],
        "beroepstype": personeelslid[0]["beroepstype"],
        "bevoegdheid": personeelslid[0]["bevoegdheid"],
        "specialist_in_attracties": [
            attractie.strip()
            for attractie in personeelslid[0]["specialist_in_attracties"].split(",")
        ],
        "pauze_opsplitsen": (
            True if personeelslid[0]["pauze_opsplitsen"] == 1 else False
        ),
        # STAP 1: vul aan met andere benodigde eigenschappen
    },
    "weergegevens": {
        # STAP 4: vul aan met weergegevens
    },
    "dagtaken": [
        {
            "omschrijving": personeelsLidTaken[0]["omschrijving"],
            "duur": personeelsLidTaken[0]["duur"],
            "prioriteit": personeelsLidTaken[0]["prioriteit"],
            "beroepstype": personeelsLidTaken[0]["beroepstype"],
            "bevoegdheid": personeelsLidTaken[0]["bevoegdheid"],
            "fysieke_belasting": personeelsLidTaken[0]["fysieke_belasting"],
            "attractie": personeelsLidTaken[0]["attractie"],
            "is_buitenwerk": personeelsLidTaken[0]["is_buitenwerk"],
        }
    ],  # STAP 2: vul aan met de juiste dagtaken
    "maximale_fysieke_belasting": maximale_fysieke_belasting,  # STAP 5: vul aan met de maximale fysieke belasting
    "totale_duur": 0,  # STAP 3: aanpassen naar daadwerkelijke totale duur
}

# uiteindelijk schrijven we de dictionary weg naar een JSON-bestand, die kan worden ingelezen door de acceptatieomgeving
with open("dagtakenlijst_personeelslid_x.json", "w") as json_bestand_uitvoer:
    json.dump(dagtakenlijst, json_bestand_uitvoer, indent=4)
