import yaml
import pandas as pd

def load_controls_from_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as file:
        yaml_data = yaml.safe_load(file)

    controls = yaml_data.get('controls', {})  # Extract the 'controls' section

    return pd.Series(controls)

def compile_specs_regions(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    region_specs = pd.DataFrame(yaml_data.get('region_specs', []))
    
    return region_specs

def compile_specs_transmission(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    transmission_specs = pd.DataFrame(yaml_data.get('transmission_specs', []))
    
    return transmission_specs

def compile_specs_storage(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    storage_specs = pd.DataFrame(yaml_data.get('storage_specs', []))
    
    return storage_specs

def compile_specs_generation(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    generation_specs = pd.DataFrame(yaml_data.get('generation_specs', []))
    
    return generation_specs

# Replace 'your_config_file.yaml' with the actual path to your YAML config file
yaml_file_path = 'config.yaml'

controls = load_controls_from_yaml(yaml_file_path)
region_specs = compile_specs_regions(yaml_file_path)
transmission_specs = compile_specs_transmission(yaml_file_path)
storage_specs = compile_specs_storage(yaml_file_path)
generation_specs = compile_specs_generation(yaml_file_path)
