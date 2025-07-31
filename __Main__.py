import tkinter.messagebox
import pandas as pd
import dearpygui.dearpygui as dpg
from dearpygui import *
import pyautogui as p
import tkinter
import csv
import glob
import time
import os

#"C:/Users/ww-in/Desktop/scan_Data"
path = "C:/Users/ww-in/Desktop/scan_Data"
_filename = ""
status = ""

def StartScanning() :
    p.click(x=509, y=740)
    p.click(x=36, y=674)
    p.click(x=420, y=741)
        #p.click(x=516, y=650)


def Interface() :
    global inputFoutPotje
    global status

    width, height = get_screen_dimensions_tkinter()

    height -= 80
    width = int(width/2)

    dpg.create_context()
    dpg.create_viewport(width=width, height=height, title="Scanner")
    dpg.setup_dearpygui()

    #def toggle_buttonStart_callback(sender, data):
    #    global status
    #    StartScanning()
    #
    #    button_data = dpg.get_item_user_data(sender)
    #    current_state = button_data['state']
    #    if current_state:
    #        dpg.bind_item_theme(sender, button_data['off_theme'])
    #        dpg.set_item_label(startbtn, "Start")
    #        dpg.set_value(statustext, "Status: Stopped")
    #        status = "Stopped"
    #        button_data['state'] = False
    #    else:
    #        # Turn on
    #        dpg.bind_item_theme(sender, button_data['on_theme'])
    #        dpg.set_item_label(startbtn, "Stop")
    #        dpg.set_value(statustext, "Status: Started")
    #        button_data['state'] = True
    #    dpg.set_item_user_data(sender, button_data)

    def toggle_buttonVerwijderen_callback(sender, data):
        Verwijderen(_filename)
        global status
        button_data = dpg.get_item_user_data(sender)
        current_state = button_data['state']
        if current_state:
            # Turn off
            dpg.bind_item_theme(sender, button_data['off_theme'])
            dpg.set_value(statustext, "Status: Stopped")
            status = "Stopped"
            button_data['state'] = False
        else:
            # Turn on
            dpg.bind_item_theme(sender, button_data['on_theme'])
            dpg.set_value(statustext, "Status: Verwijderen")
            time.sleep(0.5)
            dpg.set_value(statustext, "Status: Stopped")
            status = "Stopped"
            button_data['state'] = True
        dpg.set_item_user_data(sender, button_data)

    def toggle_buttonStartScannenVerwijderen(sender, data):
        StartScanning()
        global status
        button_data = dpg.get_item_user_data(sender)
        current_state = button_data['state']
        if current_state:
            # Turn off
            dpg.bind_item_theme(sender, button_data['off_theme'])
            dpg.set_value(statustext, "Status: Stopped")
            status ="Stopped"
            button_data['state'] = False
        else:
            # Turn on
            dpg.bind_item_theme(sender, button_data['on_theme'])
            dpg.set_value(statustext, "Status: Started scanning for Deleting")
            status = "Scanning for deleting"
            button_data['state'] = True
        dpg.set_item_user_data(sender, button_data)

    def eindeDoos() :
        dpg.set_value(statustext, "Stopped")
        StartScanning()
        combineCsv()

    def nieuweDoos():
        dpg.set_value(statustext, "Started")
        StartScanning()

    def searchForCode1() :
        searchForCode2(_filename)
        
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
        
    with dpg.theme() as Theme_input:
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (89, 96, 181), category=dpg.mvThemeCat_Core)

    with dpg.theme() as VerwijderButtonOff:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (72, 72, 74), category=dpg.mvThemeCat_Core)

    with dpg.theme() as light_theme:
        with dpg.theme_component(0):
            dpg.add_theme_color(dpg.mvThemeCol_Text                   , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled           , (0.60 * 255, 0.60 * 255, 0.60 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg               , (0.94 * 255, 0.94 * 255, 0.94 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg                , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.98 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Border                 , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.30 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow           , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg                , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg                , (0.96 * 255, 0.96 * 255, 0.96 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive          , (0.82 * 255, 0.82 * 255, 0.82 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed       , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.51 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg              , (0.86 * 255, 0.86 * 255, 0.86 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg            , (0.98 * 255, 0.98 * 255, 0.98 * 255, 0.53 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab          , (0.69 * 255, 0.69 * 255, 0.69 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered   , (0.49 * 255, 0.49 * 255, 0.49 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive    , (0.49 * 255, 0.49 * 255, 0.49 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark              , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive       , (0.46 * 255, 0.54 * 255, 0.80 * 255, 0.60 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive           , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header                 , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.31 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered          , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Separator              , (0.39 * 255, 0.39 * 255, 0.39 * 255, 0.62 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered       , (0.14 * 255, 0.44 * 255, 0.80 * 255, 0.78 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive        , (0.14 * 255, 0.44 * 255, 0.80 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip             , (0.35 * 255, 0.35 * 255, 0.35 * 255, 0.17 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered      , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive       , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab                    , (0.76 * 255, 0.80 * 255, 0.84 * 255, 0.93 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered             , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive              , (0.60 * 255, 0.73 * 255, 0.88 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused           , (0.92 * 255, 0.93 * 255, 0.94 * 255, 0.99 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive     , (0.74 * 255, 0.82 * 255, 0.91 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.22 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg         , (0.20 * 255, 0.20 * 255, 0.20 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines              , (0.39 * 255, 0.39 * 255, 0.39 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered       , (1.00 * 255, 0.43 * 255, 0.35 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram          , (0.90 * 255, 0.70 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered   , (1.00 * 255, 0.45 * 255, 0.00 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg          , (0.78 * 255, 0.87 * 255, 0.98 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong      , (0.57 * 255, 0.57 * 255, 0.64 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight       , (0.68 * 255, 0.68 * 255, 0.74 * 255, 1.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg             , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt          , (0.30 * 255, 0.30 * 255, 0.30 * 255, 0.09 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget         , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight           , (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight  , (0.70 * 255, 0.70 * 255, 0.70 * 255, 0.70 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg      , (0.20 * 255, 0.20 * 255, 0.20 * 255, 0.20 * 255))
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg       , (0.20 * 255, 0.20 * 255, 0.20 * 255, 0.35 * 255))
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg       , (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBg        , (0.42 * 255, 0.57 * 255, 1.00 * 255, 0.13 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBorder    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg      , (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.98 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBorder  , (0.82 * 255, 0.82 * 255, 0.82 * 255, 0.80 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendText    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_TitleText     , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText     , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBg        , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgActive  , (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisBgHovered , (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisGrid      , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_AxisText      , (0.00 * 255, 0.00 * 255, 0.00 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Selection     , (0.82 * 255, 0.64 * 255, 0.03 * 255, 1.00 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs    , (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.50 * 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundHovered, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundSelected, (240, 240, 240, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, (100, 100, 100, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (248, 248, 248, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (209, 209, 209, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Link, (66, 150, 250, 100), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkHovered, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkSelected, (66, 150, 250, 242), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Pin, (66, 150, 250, 160), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_PinHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelector, (90, 170, 250, 30), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelectorOutline, (90, 170, 250, 150), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridBackground, (225, 225, 225, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridLine, (180, 180, 180, 100), category=dpg.mvThemeCat_Nodes)

    with dpg.window(label="Scanner Interface", width=width, height=height):
        #with dpg.group(horizontal=True):
            #startbtn = dpg.add_button(label="Start", tag="toggle_button" ,callback=toggle_buttonStart_callback, width = 200, height = 50, pos=[(width/2)-100,50])
            #button_data = {'state': False, 'on_theme': stopButtonTheme, 'off_theme': startButtonTheme}
            #dpg.set_item_user_data("toggle_button", button_data)
            #dpg.bind_item_theme("toggle_button", stopButtonTheme)
            
        with dpg.group(horizontal=False):
            dpg.add_spacer(height=50)
            dpg.add_button(label="Start/Nieuwe Doos", callback = nieuweDoos, width = 200, height = 50, indent=50)
            dpg.add_spacer(height=20)
            dpg.add_button(label="Einde Doos", callback = eindeDoos, width = 200, height = 50, indent=50)
            dpg.add_spacer(height=30)

        with dpg.group(horizontal= True):
            inputFoutPotje = dpg.add_input_text(label = "nr fout potje", width=200, indent=50)

        dpg.add_button(label="Handmatig Verwijderen", callback=searchForCode1, width=250,height=50, indent=50)
        dpg.add_spacer(height=150)

        with dpg.group():
            VerwijderBtn = dpg.add_button(label="Verwijderen", tag="Toggle_verwijderBtn", callback=toggle_buttonVerwijderen_callback, width = 200, height = 50, indent=50)
            button_data = {'state': False, 'on_theme': VerwijderButtonOff, 'off_theme': VerwijderButtonOn}
            dpg.set_item_user_data("Toggle_verwijderBtn", button_data)
            dpg.add_spacer(height=20)

            dpg.add_button(label="Start/stop scannen (Verwijderen)", tag="Toggle_ScanStartVerwijder", callback=toggle_buttonStartScannenVerwijderen, width = 350, height = 50, indent=50)
            button_data = {'state': False, 'on_theme': VerwijderButtonOff, 'off_theme': VerwijderButtonOn}
            dpg.set_item_user_data("Toggle_ScanStartVerwijder", button_data)
            dpg.add_spacer(height=20)

        with dpg.group():
            EstopBtn = dpg.add_button(label="Emergency Stop", callback=Estop, width = 200, height = 50, pos=[width - 210, height - 80])
            statustext = dpg.add_text(default_value=f"Status: Stopped", pos=[10, height - 60], indent=50)

    #dpg.bind_item_theme(startbtn, startButtonTheme)
    dpg.bind_item_theme(EstopBtn, stopButtonTheme)
    dpg.bind_item_theme(inputFoutPotje, Theme_input)
    dpg.bind_theme(light_theme)
    dpg.show_viewport()
    dpg.set_global_font_scale(1.5)
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
    global status
    global _filename
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

        start_q5 = len(s) - 10
        q5_val = s[start_q5:] if start_q5 >= 0 else ''

        return q3_val, q4_val, q5_val

    q3_q4_results = combined_df["Datacode-1:String"].apply(lambda s: get_q3_q4_parts(s))
    combined_df[['LOT', 'UNIQUE NR', 'ORDER']] = pd.DataFrame(q3_q4_results.tolist(), index=combined_df.index)

    combined_df = combined_df.rename(columns={"Datacode-1:String" : "UDI"})

    combined_df = combined_df[combined_df['UDI'].str.len().ge(30).fillna(False)].copy()
    combined_df = combined_df[:-2]

    combined_df = combined_df.sort_values('ORDER', ignore_index=True, ascending=False)

    Final_fileName = f'(01){combined_df.iloc[0]["UDI-DI"]}(17){combined_df.iloc[0]["EXPIRY DATE"]}(10){combined_df.iloc[0]["LOT"]}(21){combined_df.iloc[0]["UNIQUE NR"]}.csv'

    combined_df = combined_df.drop(0)

    combined_df = combined_df.sort_values('ORDER', ignore_index=True)

    combined_df = combined_df.drop("ORDER", axis='columns')

    output_directory = "C:/Users/ww-in/Desktop/ScannerProgramma"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 

    output_filepath = os.path.join(output_directory, output_filename)
    combined_df.to_csv(output_filepath, index=False)

    reader = csv.reader(open("C:/Users/ww-in/Desktop/ScannerProgramma/combined_scan_data.csv", "r"), delimiter=',')
    writer = csv.writer(open("output.csv", 'w'), delimiter=';')
    writer.writerows(reader)

    with open('output.csv') as input, open(Final_fileName, 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    os.remove("output.csv")

    print(f"\nSuccessfully combined {len(all_files)} CSV files into: {output_filepath}, doc made {Final_fileName}")

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
           os.remove(file_path)
           print(filename, "is removed")

    tkinter.messagebox.showinfo(title="Data Verwerking", message=f"Data Verwerking is klaar, je kan verder gaan")
    
    status = "ready"
    _filename = Final_fileName
    return Final_fileName

def searchForCode2(_filename) :
    Openen_df = pd.read_csv("combined_scan_data.csv")

    FoutPotje = dpg.get_value(inputFoutPotje)

    try:
        Openen_df = Openen_df.drop(Openen_df[Openen_df["UNIQUE NR"] == FoutPotje].index)
    except Exception as e:
        print(f"nr {FoutPotje} not found")

    print(Openen_df)

    output_directory = "C:/Users/ww-in/Desktop/ScannerProgramma"
    output_filename = "combined_scan_data.csv"
    
    os.makedirs(output_directory, exist_ok=True) 

    output_filepath = os.path.join(output_directory, output_filename)
    Openen_df.to_csv(output_filepath, index=False)

    reader = csv.reader(open("combined_scan_data.csv", "r"), delimiter=',')
    writer = csv.writer(open("output.csv", 'w'), delimiter=';')
    writer.writerows(reader)

    with open('output.csv') as input, open(_filename, 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    os.remove("output.csv")

    print(f"done made file as {_filename}")
    tkinter.messagebox.showinfo(title="Handmatig verwijderen", message=f"{FoutPotje} is verwijderd")


def Verwijderen(_filename):
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

    df1_rows_not_in_df2.to_csv(f"{_filename}_FouteVerwijderd.csv", index=False, sep=';')

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
           os.remove(file_path)
           print(filename, "is removed")

if __name__ == "__main__":
    #combineCsv()
    #searchForCode()
    Interface()
    #Verwijderen()