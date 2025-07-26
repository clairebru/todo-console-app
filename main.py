import json
import os
import sys

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)
    
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    new_id = max([task['id'] for task in tasks], default=0) + 1
    tasks.append({'id': new_id, 'description': description, 'done': False})
    save_tasks(tasks)
    print(f"Tâche ajoutée avec l'id {new_id}.")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Aucune tâche à afficher.")
        return
    for task in tasks:
        status = "✔️" if task['done'] else "❌"
        print(f"{task['id']}: {task['description']} [{status}]")

# à compléter : fonctions done_task et delete_task

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [<args>]")
        return
    
    command = sys.argv[1]
    
    # implémenter le routage des commandes ici.

if __name__ == "__main__":
    main()