
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

    echo "$timestamp,$kilowattHours,$treesKilled,$costDollars,$userId" >> "$TRACKER_DIR/$TRACKER_FILE"
    