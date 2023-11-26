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

def load_csv_data(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    csv_file_path = yaml_data.get('csv_file_path', '')  # Get the path to the CSV file

    if csv_file_path:
        df = pd.read_csv(csv_file_path, index_col=0)
        return df
    else:
        return None
    

def load_energy_data(regionList):
    for reg in regionList['regionstorType']:
        print(reg)
        
    #     df['demand-'  + reg] = # demand data
    #     df['vreGen-'  + reg] = # VRE generation potential
    #                             #   - capacity-weighted sum of 
    #                             #     all regional PV & wind potential
    #                             #     (ignoring sub-regional transmission)
    #     # df['mustRun-'  + reg] = # must-run generators output
                                
    #     df['mm-'  + reg] = df['demand-'  + reg] - df['vreGen-'  + reg]                                        
    #     # df['mm-'  + reg] -= df['mustRun-'  + reg]
        
    # return df
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