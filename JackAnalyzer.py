
from CompilationEngine import CompilationEngine
import os

from tkinter import *
from tkinter import filedialog





def compile():
    root = Tk()
    root.withdraw()
    input_file_path = filedialog.askdirectory(initialdir = "/", title = "Select a folder")

    for file_name in os.listdir(input_file_path):
        
        if file_name.lower().endswith(".jack"):
            
            new_file_name = file_name[:file_name.find(".")]
            CompilationEngine(input_file_path + "\\" + file_name, input_file_path + "\\" + new_file_name + ".xml")

if __name__ == "__main__":
    compile()