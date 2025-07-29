import sys
import json
import pytest
from io import StringIO
import main

# Fixture to use a temporary tasks.json file in the temporary working directory.
@pytest.fixture(autouse=True)
def temp_tasks_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "tasks.json"
    monkeypatch.chdir(tmp_path)
    main.TASKS_FILE = "tasks.json"
    yield temp_file
    if temp_file.exists():
        temp_file.unlink()

def test_main_no_args(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    main.main()
    captured = capsys.readouterr().out
    assert "Usage: python main.py <command>" in captured

def test_unknown_command(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "foobar"])
    main.main()
    captured = capsys.readouterr().out
    assert "Commande inconnue : foobar" in captured

def test_handle_add_no_description(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "add"])
    main.main()
    captured = capsys.readouterr().out
    assert "Usage: python main.py add <description>" in captured

def test_handle_done_no_id(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "done"])
    main.main()
    captured = capsys.readouterr().out
    assert "Usage: python main.py done <task_id>" in captured

def test_handle_delete_no_id(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "delete"])
    main.main()
    captured = capsys.readouterr().out
    assert "Usage: python main.py delete <task_id>" in captured

def test_handle_done_invalid_id(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "done", "abc"])
    main.main()
    captured = capsys.readouterr().out
    assert "ID de tâche invalide." in captured

def test_handle_delete_invalid_id(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "delete", "abc"])
    main.main()
    captured = capsys.readouterr().out
    assert "ID de tâche invalide." in captured

def test_list_empty_tasks(capsys, temp_tasks_file):
    # Ensure tasks.json does not exist (or is empty)
    if temp_tasks_file.exists():
        temp_tasks_file.write_text("")
    main.list_tasks()
    captured = capsys.readouterr().out
    assert "Aucune tâche à afficher." in captured

def test_add_and_list(capsys, monkeypatch, temp_tasks_file):
    # Test adding a task then listing tasks
    monkeypatch.setattr(sys, "argv", ["main.py", "add", "new task"])
    main.main()
    captured = capsys.readouterr().out
    assert "Tâche ajoutée avec l'id" in captured

    monkeypatch.setattr(sys, "argv", ["main.py", "list"])
    main.main()
    captured = capsys.readouterr().out
    assert "new task" in captured

def test_done_and_delete(capsys, monkeypatch, temp_tasks_file):
    # Add a task, mark it done, then delete it.
    # Add task
    monkeypatch.setattr(sys, "argv", ["main.py", "add", "task to finish"])
    main.main()
    add_output = capsys.readouterr().out
    # Extract id from output (assumes output in format "Tâche ajoutée avec l'id X.")
    task_id = int(add_output.strip().split()[-1].rstrip("."))
    
    # Mark task as done
    monkeypatch.setattr(sys, "argv", ["main.py", "done", str(task_id)])
    main.main()
    done_output = capsys.readouterr().out
    assert f"Tâche {task_id} marquée comme terminée." in done_output

    # Delete task
    monkeypatch.setattr(sys, "argv", ["main.py", "delete", str(task_id)])
    main.main()
    delete_output = capsys.readouterr().out
    assert f"Tâche {task_id} supprimée." in delete_output