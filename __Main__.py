import pandas as pd
import dearpygui.dearpygui as dpg
import csv
import glob
import os

inputFoutPotje = ""

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

    combined_df = pd.concat(df_list, ignore_index=True).drop_duplicates(subset="Datacode-1:String", keep="first")
    
    output_directory = "C:/Users/ww-in/Desktop/Programma-Scanner"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 

    output_filepath = os.path.join(output_directory, output_filename)
    combined_df.to_csv(output_filepath, index=False)
    
    reader = csv.reader(open("combined_scan_data.csv", "r"), delimiter=',')
    writer = csv.writer(open("output.csv", 'w'), delimiter=';')
    writer.writerows(reader)

    print(f"\nSuccessfully combined {len(all_files)} CSV files into: {output_filepath}")

def searchForCode(inputFoutPotje) :
    FoutPotje = inputFoutPotje

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

    combined_df = pd.concat(df_list, ignore_index=True).drop_duplicates(subset="Datacode-1:String", keep="first")
    
    try:
        df_NoFoutPotje = combined_df[combined_df["Datacode-1:String"] != FoutPotje].copy()
    except Exception as e:
        print(f"nr {FoutPotje} not found")

    output_directory = "C:/Users/ww-in/Desktop/Programma-Scanner"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 

    output_filepath = os.path.join(output_directory, output_filename)
    df_NoFoutPotje.to_csv(output_filepath, index=False)

    reader = csv.reader(open("combined_scan_data.csv", "r"), delimiter=',')
    writer = csv.writer(open("output.csv", 'w'), delimiter=';')
    writer.writerows(reader)
    
    print(f"\nSuccessfully combined {len(all_files)} CSV files into: {output_filepath}")

def Interface() :
    dpg.create_context()
    dpg.create_viewport(width=600, height=200)
    dpg.setup_dearpygui()

    with dpg.window(label="Scanner Interface",width=600, height=200):
        dpg.add_button(label="CombineCsv", callback = combineCsv, width = 100, height = 40)
        inputFoutPotje = dpg.add_input_text(label = "nr fout potje")
        dpg.add_button(label="Fout potje", callback=searchForCode, width = 100, height = 40)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    #combineCsv()
    #searchForCode()
    Interface()