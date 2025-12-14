"""
Data Loading & Validation
"""
import yaml

def read_data(file_path="data.yaml"):
    with open(file_path) as file:
        return yaml.safe_load(file)
