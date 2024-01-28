import requests
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import time
import csv
import os


def getData():
    csv_file_path = '~/Library/Caches/energy-tracker/energy-log.txt'

    # Expand the tilde to the user's home directory
    expanded_path = os.path.expanduser(csv_file_path)

    # Check if the file exists
    if os.path.exists(expanded_path):
        # Open the CSV file
        with open(expanded_path, 'r') as csv_file:
            # Rest of your code to read the CSV file
            csv_reader = csv.reader(csv_file)
            values_list = []
            for row in csv_reader:
                for value in row:
                    values_list.append(value)

    else:
        print(f"The file {expanded_path} does not exist.")
    return {
        "time" : values_list[0],
        "energy": values_list[1],
        "killed": values_list[2],
        "cost": values_list[3],
        "device_id": values_list[4]
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
    username = ''
    while not logged_in:
        username, password = get_credentials()
        path = "login-app?username=" + username + "&password=" + password
        
        responce = requests.get(baseurl + path)
        if responce.status_code == 200:
            print ('success!')
            logged_in = True
        
    while True:
        data = getData()
        data['user'] = username
        path = "create-dp"
        responce = requests.post(baseurl + path, json=data)
        time.sleep(5)