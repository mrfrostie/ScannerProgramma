import pandas as pd
import glob
import os

def combineCsv () :
    path = r'C:\Users\ww-in\Desktop\scan_Data' 
    all_files = glob.glob(os.path.join(path , "/*.csv"))

    

if "__Main__" == __name__ :
    combineCsv();