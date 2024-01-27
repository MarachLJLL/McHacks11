import requests
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import time

def calcEnergy():
    return 9001

def getData():
    # only get data if certain conditions are met (charging)
    return {
        "energy": calcEnergy(),
        "time": datetime.now().isoformat(),
    }

def get_credentials():
    root = tk.Tk()
    root.withdraw()  # hide the main window

    # Get username
    username = simpledialog.askstring("Username", "Enter your username:", parent=root)

    # Get password
    password = simpledialog.askstring("Password", "Enter your password:", parent=root, show='*')

    root.destroy()
    return username, password

if __name__ == "__main__":
    baseurl = "http://127.0.0.1:5000/"
    logged_in = False

    while not logged_in:
        username, password = get_credentials()
        path = "login?username=" + username + "?password=" + password
        responce = requests.get(baseurl + path)
        if responce.status_code == 200:
            logged_in = True
    
    while True:
        data = getData()
        path = "create-dp"
        responce = requests.post(baseurl + path, json=data)
        print(responce.text)
        time.sleep(5 * 60)