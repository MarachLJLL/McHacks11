import os
import subprocess
import urllib.request

def create_local_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

def install_energy_tracker():
    # Define content for the bash script and cron script
    log_script_content = """
    # GLOBALS
    TRACKER_DIR=~/Library/Caches/energy-tracker 
    TRACKER_FILE=energy-log.txt
    IOREG=/usr/sbin/ioreg

    # PREREQUISITES
    mkdir -p ~/Library/Caches/energy-tracker

    if ! command -v $IOREG &> /dev/null
    then
        echo "ioreg not found"
        exit 1
    fi

    # Compute energy usage
    wattage=`$IOREG -rw0 -c AppleSmartBattery | grep BatteryData | grep -o '"AdapterPower"=[0-9]*' | cut -c 16- | xargs -I %  lldb --batch -o "print/f %" | grep -o '$0 = [0-9.]*' | cut -c 6-`
    kilowattHours=$(bc -l <<<"${wattage}/60*0.001")

    # Get user ID
    userId=$(id -u $(whoami))

    # compute trees killed
    treesKilled=$(bc -l <<<"${kilowattHours} * 2.588411090818529")
    # input kwh from user x 155.9 g CO2e/kWh canadian CO2 consumption x 1 tree per day / 60.23 g CO2e sequestered
    # canadian co2 consumption for grid electricity: https://www.canada.ca/en/environment-climate-change/services/managing-pollution/fuel-life-cycle-assessment-model/updated-carbon-intensity-electricity.html 
    # average carbon sequestration of a tree = 22 kg/ year from:
    # https://www.eea.europa.eu/articles/forests-health-and-climate-change/key-facts/trees-help-tackle-climate-change

    # compute cost in dollars
    costDollars=$(bc -l <<<"${kilowattHours} * 0.192")
    # national monthly avg of 19.2 Canadian cents per kilowatt-hour in 2023
    # https://www.statista.com/statistics/516279/electricity-costs-for-end-users-canada-by-province/

    timestamp=`date -u +"%Y-%m-%dT%H:%M:%SZ"`

    echo "$timestamp,$kilowattHours,$treesKilled,$costDollars,$userId" > "$TRACKER_DIR/$TRACKER_FILE"
    """

    cron_script_content = """
    * * * * * /usr/local/bin/log-power-usage.sh >> /tmp/energy-tracker.log 2>&1
    """

    # Create local files for the bash script and cron script
    create_local_file(log_script_content, "log-power-usage.sh")
    create_local_file(cron_script_content, "cron")

    # Make bash script executable
    subprocess.run(["chmod", "+x", "log-power-usage.sh"])

    # Copy the bash script to /usr/local/bin/ 
    subprocess.run(["sudo", "cp", "log-power-usage.sh", "/usr/local/bin/"])

    # Read cron file content and append to user's crontab
    cron_content = ""
    with open("cron", "r") as cron_file:
        cron_content = cron_file.read()

    subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, text=True) 
    with open("cron-new", "a") as new_cron:
        new_cron.write(cron_content)

    subprocess.run(["crontab", "cron-new"])
    subprocess.run(["rm", "cron-new"])

    # Note: Now, log-power-usage.sh and cron are used from local files

    # You can find the necessary file in the local file ~/Library/Caches/energy-tracker/energy-log.txt
if __name__ == "__main__":
    install_energy_tracker()
