import pandas as pd
import json
from pathlib import Path

def convert_csv_to_json(csv_file_path, json_file_path=None):
    """
    Convert a CSV file to JSON format with a structured output.
    
    Args:
        csv_file_path (str): Path to the input CSV file
        json_file_path (str, optional): Path to save the output JSON file. 
                                      If None, will use the same name as CSV with .json extension
    
    Returns:
        dict: The converted data in dictionary format
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Convert DataFrame to list of dictionaries
    data = df.to_dict('records')
    
    # If no output path specified, create one based on input filename
    if json_file_path is None:
        json_file_path = str(Path(csv_file_path).with_suffix('.json'))
    
    # Write to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    print(f"Successfully converted {csv_file_path} to {json_file_path}")
    return data

if __name__ == "__main__":
    # Input CSV file path
    input_csv = r"c:\Users\Vinam\CascadeProjects\geopolitical_risk_agent\geopolitical_risk_report_20250707_231940.csv"
    
    # Convert CSV to JSON
    convert_csv_to_json(input_csv)
