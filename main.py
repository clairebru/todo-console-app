import json
import os
import sys

TASKS_FILE = 'tasks.json'

# Chargement des tâches, gère les fichiers vides ou invalides
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []

# Sauvegarde des tâches dans le fichier JSON  
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Ajoute une nouvelle tâche
def add_task(description):
    tasks = load_tasks()
    new_id = max([task['id'] for task in tasks], default=0) + 1
    tasks.append({'id': new_id, 'description': description, 'done': False})
    save_tasks(tasks)
    print(f"Tâche ajoutée avec l'id {new_id}.")

# Liste les tâches existantes
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Aucune tâche à afficher.")
        return
    for task in tasks:
        status = "✔️" if task['done'] else "❌"
        print(f"{task['id']}: {task['description']} [{status}]")

# Marque une tâche comme terminée
def done_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            save_tasks(tasks)
            print(f"Tâche {task_id} marquée comme terminée.")
            return
    print(f"Tâche {task_id} non trouvée.")

# Supprime une tâche
def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Tâche {task_id} supprimée.")
            return
    print(f"Tâche {task_id} non trouvée.")

# Gestion des commandes en ligne de commande
def handle_add():
    if len(sys.argv) < 3:
        print("Usage: python main.py add <description>")
        return
    description = ' '.join(sys.argv[2:])
    add_task(description)

def handle_list():
    list_tasks()

def handle_done():
    if len(sys.argv) < 3:
        print("Usage: python main.py done <task_id>")
        return
    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("ID de tâche invalide.")
        return
    done_task(task_id)

def handle_delete():
    if len(sys.argv) < 3:
        print("Usage: python main.py delete <task_id>")
        return
    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("ID de tâche invalide.")
        return
    delete_task(task_id)

# Point d'entrée principal du programme
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [<args>]")
        return

    dispatch = {
        'add': handle_add,
        'list': handle_list,
        'done': handle_done,
        'delete': handle_delete,
    }

    command = sys.argv[1]
    action = dispatch.get(command)
    if action:
        action()
    else:
        print(f"Commande inconnue : {command}")
        print("Commandes disponibles: add, list, done, delete")
        return
    
    if len(load_tasks()) > 0:
        save_tasks(load_tasks())  # Save tasks after any operation

if __name__ == "__main__":
    main()