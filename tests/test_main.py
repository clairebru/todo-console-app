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
