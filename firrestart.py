import psutil
import os
import time
import tkinter as tk
from tkinter import messagebox

MEMORY_LIMIT = 5 * 1024 * 1024 * 1024

CHECK_INTERVAL = 120 

SLEEP_DURATION = 2 * 60 * 60

firefox_path = r"C:/Program Files/Mozilla Firefox/firefox.exe"

def get_firefox_memory_usage():
    return sum(
        proc.info['memory_info'].rss
        for proc in psutil.process_iter(['name', 'memory_info'])
        if 'firefox' in proc.info['name'].lower()
    )


def restart_firefox():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'firefox' in proc.info['name'].lower():
            os.system(f"taskkill /F /PID {proc.info['pid']}")
    time.sleep(2)
    os.system(f'"{firefox_path}"')

def show_warning_and_decide():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  
    root.focus_force()    
    user_choice = messagebox.askyesno(
        "Превышение памяти Firefox",
        "Firefox использует более 5 ГБ памяти. Перезагрузить браузер?"
    )
    root.destroy()
    return user_choice


def monitor_firefox():
    while True:
        total_memory = get_firefox_memory_usage()
        if total_memory > MEMORY_LIMIT:
            if show_warning_and_decide():
                restart_firefox()
            else:
                time.sleep(SLEEP_DURATION)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_firefox()
