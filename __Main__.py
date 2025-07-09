import pandas as pd
import dearpygui.dearpygui as dpg
from dearpygui import *
import pyautogui as p
import tkinter
import csv
import glob
import os
import re 

path = "C:/Users/seppe/Desktop/Scan_Data"

def Interface() :
    global inputFoutPotje
    width, height = get_screen_dimensions_tkinter()

    dpg.create_context()
    dpg.create_viewport(width=width, height=height)
    dpg.setup_dearpygui()

    with dpg.window(label="Scanner Interface", width=width, height=height):
        with dpg.group(horizontal=True):
            startbtn = dpg.add_button(label="Start", callback=startScanning, width = 200, height = 50, pos=[(width/2)-210,50])
            stopbtn = dpg.add_button(label="stop", callback=startScanning, width = 200, height = 50, pos=[width/2,50])
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
    
def get_screen_dimensions_tkinter():
    root = tkinter.Tk()
    root.withdraw()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.destroy() 
    return screen_width, screen_height

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
    combined_df = combined_df[['Datacode-1:String']]  
    
    combined_df["UDI-DI"] = combined_df["Datacode-1:String"].str.slice(2,16)
    combined_df["EXPIRY DATE"] = combined_df["Datacode-1:String"].str.slice(18,24)
    
    def get_q3_q4_parts(s):
        if not isinstance(s, str):
            return None, None 
        
        start_q3 = 26
        end_q3 = len(s) - 14
        q3_val = s[start_q3:end_q3] if start_q3 < end_q3 else '' 

        start_q4 = len(s) - 12
        q4_val = s[start_q4:] if start_q4 >= 0 else ''

        return q3_val, q4_val

    q3_q4_results = combined_df["Datacode-1:String"].apply(lambda s: get_q3_q4_parts(s))
    combined_df[['LOT', 'UNIQUE NR']] = pd.DataFrame(q3_q4_results.tolist(), index=combined_df.index)

    combined_df = combined_df.rename(columns={"Datacode-1:String" : "UDI"})

    Final_fileName = f'(01){combined_df.iloc[0]["UDI-DI"]}(17){combined_df.iloc[0]["EXPIRY DATE"]}(10){combined_df.iloc[0]["LOT"]}(21){combined_df.iloc[0]["UNIQUE NR"]}.csv'

    combined_df = combined_df.drop(0)

    output_directory = "C:/Users/seppe/Desktop/ScannerProgramma"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 

    output_filepath = os.path.join(output_directory, output_filename)
    combined_df.to_csv(output_filepath, index=False)

    
    reader = csv.reader(open("combined_scan_data.csv", "r"), delimiter=',')
    writer = csv.writer(open("output.csv", 'w'), delimiter=';')
    writer.writerows(reader)

    with open('output.csv') as input, open(Final_fileName, 'w', newline='') as output:
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