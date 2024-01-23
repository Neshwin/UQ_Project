import glob
import os
import pandas as pd

def process_region_data(folder_path):
    # Use glob to get a list of all CSV files in the folder
    csv_files = glob.glob(f"{folder_path}/*.csv")

    # Initialize DataFrames for Region1 (CNQ, GG, SQ) and Region2 (all others)
    region1_data = None
    region2_data = None

    # Iterate through CSV files
    for csv_file in csv_files:
        region_name = os.path.basename(csv_file).split('_')[0]
        
        # Read the CSV file into a DataFrame
        file = pd.read_csv(csv_file)
        
        # Check if Region1 or Region2 and add data to the respective DataFrame
        if region_name in ['CNQ', 'GG', 'SQ']:
            if region1_data is None:
                region1_data = file[['Year', 'Month', 'Day']]
            region1_data = region1_data.add(file.iloc[:, 3:], fill_value=0)
        else:
            if region2_data is None:
                region2_data = file[['Year', 'Month', 'Day']]
            region2_data = region2_data.add(file.iloc[:, 3:], fill_value=0)

    # Save the resulting DataFrames to new CSV files
    region1_data=region1_data[region1_data.Year==2050]
    region1_data=region1_data[region1_data.Year==2050]
    region1_data.to_csv('region1_data.csv', index=False)
    region2_data.to_csv('region2_data.csv', index=False)

    return region1_data, region2_data

# Replace 'your_folder_path' with the actual folder path
folder_path = r'C:\Users\neshw\Downloads\transfer_3149706_files_9c6f249d (1)\demand_step_change\demand_step_change'

# Call the function
region1_data, region2_data = process_region_data(folder_path)

