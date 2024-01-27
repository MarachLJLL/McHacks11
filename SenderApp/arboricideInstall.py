import os
import subprocess
import urllib.request

def download_file(url, destination):
    urllib.request.urlretrieve(url, destination)

def install_energy_tracker():
    # Download bash script and cron script
    download_file("https://raw.githubusercontent.com/rdegges/energy-tracker/main/log-power-usage.sh", "log-power-usage.sh")
    download_file("https://raw.githubusercontent.com/rdegges/energy-tracker/main/cron", "cron")

    # Make bash script executable
    subprocess.run(["chmod", "+x", "log-power-usage.sh"])

    subprocess.run(["sudo", "cp", "log-power-usage.sh", "/usr/local/bin/"])

    subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, text=True) 
    with open("cron-new", "a") as new_cron:
        subprocess.run(["cat", "cron"], stdout=new_cron, text=True)

    subprocess.run(["crontab", "cron-new"])
    subprocess.run(["rm", "cron-new"])

    print("Energy tracker installed and cron job set up successfully.")

if __name__ == "__main__":
    install_energy_tracker()
