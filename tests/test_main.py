import os
import pytest
import json

import main # Importing the main module to test its functionality

# Fixture to create a temporary file for testing
@pytest.fixture(autouse=True)
def clean_tasks_file(tmp_path, monkeypatch):
    fake = tmp_path / "tasks.json"
    monkeypatch.chdir(tmp_path) # Change the working directory to the temp path
    return fake

def test_load_empty_file(clean_tasks_file):
    # No tasks.json file should return an empty list
    assert main.load_tasks() == []

def test_add_and_save_and_load_task(clean_tasks_file):
    # Add a task and check if it is saved and loaded correctly
    main.add_task("Test task")
    data = json.loads(clean_tasks_file.read_text(encoding='utf-8'))
    assert isinstance(data, list) and data[0]["description"] == "Test task"

def test_done_task(clean_tasks_file):
    # Add a task, mark it as done, and check if it is updated correctly
    clean_tasks_file.write_text('[{"id": 1, "description": "X", "done": false}]')
    main.done_task(1)
    content = json.loads(clean_tasks_file.read_text(encoding='utf-8'))
    assert content[0]["done"] is True

def test_delete_task(clean_tasks_file):
    # Add a task, delete it, and check if it is removed from the list
    tasks = [{"id": 1, "description": "A", "done": False},
             {"id": 2, "description": "B", "done": False},
             ]
    clean_tasks_file.write_text(json.dumps(tasks))
    main.delete_task(1)
    remaining = json.loads(clean_tasks_file.read_text(encoding='utf-8'))
    assert len(remaining) == 1 and remaining[0]["id"] == 2