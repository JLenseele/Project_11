<a name="readme-top"></a>
# Güdlft

Application Web permettant à divers club régionnaux de reserver des places sur divers événements et compétitions de force.

## Features

- Connexion via le mail du club
- Réservation de places pour une compétition

## Requirements

+ [Python v3+](https://www.python.org/downloads/)
+ [Flask](https://flask.palletsprojects.com/en/1.1.x/)
+ [Pytest](https://docs.pytest.org/en/7.3.x/)

## Installation & Get Started

#### Récuperer le projet sur GitHub

    git clone https://github.com/JLenseele/Project_11.git
    cd project_11

#### Créer l'environement virtuel

    python -m venv env
    env\Scripts\activate
    pip install -r requierments.txt
    
#### Lancer les tests  

    pytest -s
    
##### Couverture de tests

creer un fichier .coveragerc avec ce contenu

    [run]
    omit = GUDLFT_app/tests/*

générer un rapport de couverture de test

    pytest --cov=. --cov-report html

#### Lancer le serveur

Depuis Windows, lancer cette commande depuis powershell

    $env:FLASK_APP = "run.py"

puis sur le terminal

    python -m flask run
    
L'application est désormais disponible depuis l'URL :
    
    http://127.0.0.1:5000/

## Utilisation

Depuis votre navigateur, ouvrez l'URL suivant : 

    http://127.0.0.1:5000/ (application web)  
    
Vous pourrez ensuite vous connecter avec l'un des identifiants présent dans le fichier club.json fourni

## Current Setup

Cette application fonctionne avec des fichiers JSON comme BDD [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm).
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributors

[JLenseele](https://github.com/JLenseele)

