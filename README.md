# To-Do List Console

Cette application en ligne de commande permet de gérer une liste de tâches :
- Ajouter (`add <description>`)
- Lister (`list`)
- Marquer comme faite (`done <id>`)
- Supprimer (`delete <id>`)

## Installation

py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt

## Usage

py main.py add "Acheter du pain"
py main.py list
py main.py done 2
py main.py delete 3