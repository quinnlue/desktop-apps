import requests
import random, os
import ctypes
import tkinter as tk
from tkinter import *
import json
import time
import shutil
import sys
import winshell
from win32com.client import Dispatch
import subprocess

def run_exe():
    os.system(os.path.join(f"{os.getenv('APPDATA')}\\QL_Desktop_Changer", "change_wallpaper.exe"))

def find_config():
    try:
        config_path = os.path.join(f"{os.getenv('APPDATA')}\\QL_Desktop_Changer", "config.json")
        with open(config_path, 'r') as file:
            config = json.load(file)
    except:
        config = move_files()

    config_path = os.path.join(f"{os.getenv('APPDATA')}\\QL_Desktop_Changer", "config.json")
    return config, config_path


def move_files():
    def create_appdata_folder():
        appdata_path = os.getenv('APPDATA')
        app_folder = os.path.join(appdata_path, 'QL_Desktop_Changer')
        if not os.path.exists(app_folder):
            os.makedirs(app_folder)
        return app_folder

    def move_config_and_images(src_folder, dest_folder):
        shutil.move(os.path.join(os.path.dirname(src_folder), 'config.json'), dest_folder)
        shutil.move(src_folder, os.path.join(dest_folder, 'images'))
        shutil.move(os.path.join(os.path.dirname(src_folder), "change_wallpaper.exe"), dest_folder)
    def run():
        def get_script_dir():
            if getattr(sys, 'frozen', False):
                script_dir = os.path.dirname(sys.executable)
            else:
                script_dir = os.path.dirname(os.path.abspath(__file__))
            return script_dir

        script_dir = get_script_dir()
        src_folder = os.path.join(script_dir, "images")


        dest_folder = create_appdata_folder()
        move_config_and_images(src_folder, dest_folder)
    run()
    config_path = os.path.join(f"{os.getenv('APPDATA')}\\QL_Desktop_Changer", "config.json")
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config


def write_config(config_input, config, config_path):
    existing_config = config
    existing_config.update(config_input)
    with open(config_path, 'w') as file:
        json.dump(existing_config, file)
    file.close()
    return

def open_gui(config, config_path):

    def button():
        global new_config
        new_config = {}
        query = city_entry.get() + ' ' + region_entry.get() + ' ' + country_entry.get()
        try:
            interval = 60 * int(interval_entry.get())
        except:
            interval = 60 * 15

        new_config['location'] = query
        new_config['interval'] = interval
        new_config['on_startup'] = (on_startup_var.get()==1)
        
    window = Tk()
    window.title("Desktop Weather")
    window.geometry('230x160')

    l1 = Label(window,text='Location')
    l2 = Label(window,text='City')
    l3 = Label(window,text='Region')
    l4 = Label(window,text='Country')

    l5 = Label(window,text="Interval (m)")
    l6 = Label(window,text="On Startup")

    city_entry = Entry(window)
    region_entry = Entry(window)
    country_entry = Entry(window)
    interval_entry = Entry(window)
    on_startup_var = IntVar()
    on_startup_entry = Checkbutton(window, variable=on_startup_var)
    submit_button = Button(window, text='Submit', command=button)
    submit_button.grid(column=2,row=7)
    l1.grid(column=2,row=1)
    l2.grid(column=1,row=2,columnspan=1)
    l3.grid(column=1,row=3,columnspan=1)
    l4.grid(column=1,row=4,columnspan=1)
    l5.grid(column=1,row=5)
    l6.grid(column=1,row=6)
    city_entry.grid(column=2,row=2,columnspan=2)
    region_entry.grid(column=2,row=3,columnspan=2)
    country_entry.grid(column=2,row=4,columnspan=2)
    interval_entry.grid(column=2,row=5,columnspan=2)
    on_startup_entry.grid(column=2,row=6,columnspan=2)
    
    window.mainloop()

    write_config(new_config, config, config_path)

def create_startup_shortcut():
    path = os.path.join(f"{os.getenv('APPDATA')}\\QL_Desktop_Changer", "change_wallpaper.exe")

    shortcut_name = "desktop_change.lnk"
    

    on_startup = os.path.join(winshell.startup(), shortcut_name)
    

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(on_startup)
    shortcut.TargetPath = path

    shortcut.WorkingDirectory = os.path.dirname(path)
    shortcut.save()

    
if __name__ == "__main__":
    create_startup_shortcut()
    config, config_path = find_config()
    open_gui(config, config_path)
    run_exe()