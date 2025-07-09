import pandas as pd
import dearpygui.dearpygui as dpg
from dearpygui import *
import pyautogui as p
import csv
import glob
import os


path = "C:/Users/seppe/Desktop/Scan_Data"

def Interface() :
    global inputFoutPotje
    dpg.create_context()
    dpg.create_viewport(width=2000, height=1000)
    dpg.setup_dearpygui()


    with dpg.window(label="Scanner Interface",width=2000, height=1000):
        with dpg.group(horizontal=True):
            startbtn = dpg.add_button(label="Start", callback=startScanning, width = 200, height = 50)
            stopbtn = dpg.add_button(label="stop", callback=startScanning, width = 200, height = 50)
        dpg.add_button(label="Nieuwe Doos", callback = combineCsv, width = 200, height = 50)
        inputFoutPotje = dpg.add_input_text(label = "nr fout potje")
        dpg.add_button(label="Fout potje", callback=searchForCode, width = 200, height = 50)

    with dpg.theme() as startButtonTheme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
    
    with dpg.theme() as stopButtonTheme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)

    dpg.bind_item_theme(startbtn, startButtonTheme)
    dpg.bind_item_theme(stopbtn, stopButtonTheme)
    dpg.show_viewport()
    dpg.set_global_font_scale(1.5)
    dpg.maximize_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    
def startScanning() :
    p.click(x=432, y=1051)
    p.click(x=59, y=961)
    p.click(x=479, y=1044)

def combineCsv():
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

    combined_df["Datacode-1:String"] = combined_df["Datacode-1:String"].str.replace("","")
    combined_df.drop(combined_df.columns.difference(['Datacode-1:String']), 1, inplace=True)
    
    output_directory = "C:/Users/seppe/Desktop/ScannerProgramma"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 

    output_filepath = os.path.join(output_directory, output_filename)
    combined_df.to_csv(output_filepath, index=False)
    
    reader = csv.reader(open("combined_scan_data.csv", "r"), delimiter=',')
    writer = csv.writer(open("output.csv", 'w'), delimiter=';')
    writer.writerows(reader)

    with open('output.csv') as input, open('ouput2.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    os.remove("output.csv")

    print(f"\nSuccessfully combined {len(all_files)} CSV files into: {output_filepath}")

    #for filename in os.listdir(path):
    #    file_path = os.path.join(path, filename)
    #    if os.path.isfile(file_path):
    #       os.remove(file_path)
    #       print(filename, "is removed")

def searchForCode() :
    FoutPotje = dpg.get_value(inputFoutPotje)
    
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
    
    combined_df["Datacode-1:String"] = combined_df["Datacode-1:String"].str.replace("","")

    try:
        df_NoFoutPotje = combined_df[combined_df["Datacode-1:String"] != FoutPotje].copy()
    except Exception as e:
        print(f"nr {FoutPotje} not found")

    output_directory = "C:/Users/seppe/Desktop/ScannerProgramma"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 

    output_filepath = os.path.join(output_directory, output_filename)
    df_NoFoutPotje.to_csv(output_filepath, index=False)

    reader = csv.reader(open("combined_scan_data.csv", "r"), delimiter=',')
    writer = csv.writer(open("output.csv", 'w'), delimiter=';')
    writer.writerows(reader)

    with open('output.csv') as input, open('ouput2.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    os.remove("output.csv")
    
    print(f"\nSuccessfully combined {len(all_files)} CSV files into: {output_filepath}")

if __name__ == "__main__":
    #combineCsv()
    #searchForCode()
    Interface()