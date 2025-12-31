"""Test file to load expense CRUD scenarios from feature file."""
from pytest_bdd import scenarios

# Step definitions are loaded via pytest_plugins in conftest.py
# Load all scenarios from the feature file
# The path is relative to bdd_features_base_dir (tests/features) in pytest.ini
scenarios("expense_crud.feature")

