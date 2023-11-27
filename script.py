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

# def load_csv_data(yaml_file_path):
#     with open(yaml_file_path, 'r', encoding='utf-8') as file:
#         yaml_data = yaml.safe_load(file)

#     csv_file_path = yaml_data.get('csv_file_path', '')  # Get the path to the CSV file

#     if csv_file_path:
#         df = pd.read_csv(csv_file_path, index_col=0)
#         return df
#     else:
#         return None
    
def load_csv_data(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    csv_files = yaml_data.get('csv_files', [])  # Get the list of CSV files

    dfs = {}
    for csv_file in csv_files:
        name = csv_file.get('name', '')
        path = csv_file.get('path', '')

        if name and path:
            df = pd.read_csv(path, index_col=0)
            dfs[name] = df

    return dfs
def load_energy_data(regionList,load_data):
    df = pd.DataFrame()
    for reg in regionList['regionstorType']:
        print(reg)
        # df = pd.DataFrame()
        df['demand-'  + reg]=load_data['load_data'][reg]
        print(len(df))
        generation = pd.Series(0, index=load_data['profiles'].index)
        # print(len(generation))
        for carrier in load_data['VRE'].index:
            print(carrier)
            generation+=load_data['profiles'][carrier]*load_data['VRE'][reg][carrier]
        df['vreGen-'  + reg] = generation     
        df['mm-'  + reg] = df['demand-'  + reg] - df['vreGen-'  + reg]
        # print(len(df))
                        
    return df
# Replace 'your_config_file.yaml' with the actual path to your YAML config file
yaml_file_path = 'config.yaml'
load_data = load_csv_data(yaml_file_path)

mismatch = load_energy_data(regionList,load_data)
controls = load_controls_from_yaml(yaml_file_path)
region_specs = compile_specs_regions(yaml_file_path)
transmission_specs = compile_specs_transmission(yaml_file_path)
storage_specs = compile_specs_storage(yaml_file_path)
generation_specs = compile_specs_generation(yaml_file_path)
regionList   = compile_specs_regions(yaml_file_path)
csv_data = load_csv_data(yaml_file_path)