import pandas as pd
import dearpygui.dearpygui as dpg
from dearpygui import *
import pyautogui as p
import tkinter
import csv
import glob
import os


path = "C:/Users/seppe/Desktop/Scan_Data"
_filename = ""

def StartScanning() :
    p.click(x=432, y=1051)
    p.click(x=59, y=961)
    p.click(x=479, y=1044)

def Interface() :
    global inputFoutPotje
    width, height = get_screen_dimensions_tkinter()

    height -= 80

    dpg.create_context()
    dpg.create_viewport(width=width, height=height)
    dpg.setup_dearpygui()

    def toggle_buttonStart_callback(sender, data):
        
        StartScanning()

        button_data = dpg.get_item_user_data(sender)
        current_state = button_data['state']
        if current_state:
            dpg.bind_item_theme(sender, button_data['off_theme'])
            dpg.set_item_label(startbtn, "Start")
            dpg.set_value(statustext, "Status: Stopped")
            button_data['state'] = False
        else:
            # Turn on
            dpg.bind_item_theme(sender, button_data['on_theme'])
            dpg.set_item_label(startbtn, "Stop")
            dpg.set_value(statustext, "Status: Started")
            button_data['state'] = True
        dpg.set_item_user_data(sender, button_data)

    def toggle_buttonVerwijderen_callback(sender, data):
        Verwijderen(_filename)

        button_data = dpg.get_item_user_data(sender)
        current_state = button_data['state']
        if current_state:
            # Turn off
            dpg.bind_item_theme(sender, button_data['off_theme'])
            dpg.set_value(statustext, "Status: Stopped")
            button_data['state'] = False
        else:
            # Turn on
            dpg.bind_item_theme(sender, button_data['on_theme'])
            dpg.set_value(statustext, "Status: Verwijderen")
            button_data['state'] = True
        dpg.set_item_user_data(sender, button_data)

    def eindeDoos() :
        #StartScanning()
        _filename = combineCsv()
        
    with dpg.theme() as startButtonTheme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
    
    with dpg.theme() as stopButtonTheme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
    
    with dpg.theme() as VerwijderButtonOn:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (102, 103, 105), category=dpg.mvThemeCat_Core)
        
    with dpg.theme() as VerwijderButtonOff:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (72, 72, 74), category=dpg.mvThemeCat_Core)


    with dpg.window(label="Scanner Interface", width=width, height=height):
        with dpg.group(horizontal=True):
            startbtn = dpg.add_button(label="Start", tag="toggle_button" ,callback=toggle_buttonStart_callback, width = 200, height = 50, pos=[(width/2)-100,50])
            button_data = {'state': False, 'on_theme': stopButtonTheme, 'off_theme': startButtonTheme}
            dpg.set_item_user_data("toggle_button", button_data)
            dpg.bind_item_theme("toggle_button", stopButtonTheme)

        dpg.add_button(label="Einde Doos", callback = eindeDoos, width = 200, height = 50)
        inputFoutPotje = dpg.add_input_text(label = "nr fout potje")

        with dpg.group(horizontal=True):
            VerwijderBtn = dpg.add_button(label="Verwijderen", tag="Toggle_verwijderBtn", callback=toggle_buttonVerwijderen_callback, width = 200, height = 50)
            button_data = {'state': False, 'on_theme': VerwijderButtonOff, 'off_theme': VerwijderButtonOn}
            dpg.set_item_user_data("Toggle_verwijderBtn", button_data)
            dpg.bind_item_theme("Toggle_verwijderBtn", VerwijderButtonOn)
    
        with dpg.group():
            EstopBtn = dpg.add_button(label="Emergency Stop", callback=Estop, width = 200, height = 50, pos=[width - 210, height - 60])
            statustext = dpg.add_text(default_value=f"Status: Stopped", pos=[10, height - 60])


    dpg.bind_item_theme(startbtn, startButtonTheme)
    dpg.bind_item_theme(EstopBtn, stopButtonTheme)
    dpg.show_viewport()
    dpg.set_global_font_scale(1.5)
    dpg.maximize_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def Estop() :
    os._exit(0)

def get_screen_dimensions_tkinter():
    root = tkinter.Tk()
    root.withdraw()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.destroy() 
    return screen_width, screen_height

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

    return Final_fileName

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

    try:
        df_NoFoutPotje = combined_df[combined_df["UDI"] != FoutPotje].copy()
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

    with open('output.csv') as input, open(Final_fileName, 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    os.remove("output.csv")
    
    print(f"\nSuccessfully combined {len(all_files)} CSV files into: {output_filepath}")

def Verwijderen(_filename):
    all_files = glob.glob(os.path.join("TeverwijderenTest", "*.csv"))

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
    print(combined_df)

    Complete_csv_path = "combined_scan_data.csv"

    complete_df = pd.read_csv(Complete_csv_path)
    print("CSV file successfully loaded into a DataFrame.")

    complete_df = complete_df[['UDI']]  
    complete_df = complete_df.rename(columns={'UDI' : 'Datacode-1:String'})
    print(complete_df)

    merged_df = pd.merge(complete_df, combined_df, on='Datacode-1:String', how='left', indicator=True)
    df1_rows_not_in_df2 = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')


    df1_rows_not_in_df2["UDI-DI"] = df1_rows_not_in_df2["Datacode-1:String"].str.slice(2,16)
    df1_rows_not_in_df2["EXPIRY DATE"] = df1_rows_not_in_df2["Datacode-1:String"].str.slice(18,24)
    
    def get_q3_q4_parts(s):
        if not isinstance(s, str):
            return None, None 
        
        start_q3 = 26
        end_q3 = len(s) - 14
        q3_val = s[start_q3:end_q3] if start_q3 < end_q3 else '' 

        start_q4 = len(s) - 12
        q4_val = s[start_q4:] if start_q4 >= 0 else ''

        return q3_val, q4_val

    q3_q4_results = df1_rows_not_in_df2["Datacode-1:String"].apply(lambda s: get_q3_q4_parts(s))
    df1_rows_not_in_df2[['LOT', 'UNIQUE NR']] = pd.DataFrame(q3_q4_results.tolist(), index=df1_rows_not_in_df2.index)

    df1_rows_not_in_df2 = df1_rows_not_in_df2.rename(columns={"Datacode-1:String" : "UDI"})

    #Final_fileName = f'(01){df1_rows_not_in_df2.iloc[0]["UDI-DI"]}(17){df1_rows_not_in_df2.iloc[0]["EXPIRY DATE"]}(10){df1_rows_not_in_df2.iloc[0]["LOT"]}(21){df1_rows_not_in_df2.iloc[0]["UNIQUE NR"]}.csv'

    df1_rows_not_in_df2.to_csv(_filename, index=False, sep=';')

if __name__ == "__main__":
    #_filename = combineCsv()
    #searchForCode()
    Interface()
    #Verwijderen(_filename)