import pandas as pd
import glob
import os

def combineCsv():
    path = "C:/Users/ww-in/Desktop/scan_Data"
    
    all_files = glob.glob(os.path.join(path, "*.csv"))

    if not all_files:
        print(f"No CSV files found in the directory: {path}")
        return 

    df_list = []
    for file in all_files:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
            print(f"Successfully read: {os.path.basename(file)}") 
        except Exception as e:
            print(f"Error reading {file}: {e}") 

    if not df_list:
        print("No DataFrames were successfully read to concatenate.")
        return 

    combined_df = pd.concat(df_list, ignore_index=True)
    
    output_directory = "C:/Users/ww-in/Desktop/Programma-Scanner"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 
    
    output_filepath = os.path.join(output_directory, output_filename)
    combined_df.to_csv(output_filepath, index=False)
    
    print(f"\nSuccessfully combined {len(all_files)} CSV files into: {output_filepath}")

if __name__ == "__main__":
    combineCsv()