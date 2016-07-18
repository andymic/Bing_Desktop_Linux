#!/bin/bash

echo "------------------------"
echo "| BING DESKTOP (Linux) |"
echo "------------------------"

SCRIPT_LOCATION="/home/$USER/background/background.py"
LOGFILE_LOCATION="/home/$USER/background/background.log"
PYTHON=$(which python3)

echo "creating dir /home/$USER/background"
mkdir -p /home/$USER/background

cp background.py /home/$USER/background
#kill any running instances
pkill -f background.py

#current crontab
crontab -l >/dev/null 2>&1 && > bing_linux_cron

#adding adding environment variables and new crontab
echo "Setting up cron job"
echo "SHELL="$SHELL >> bing_linux_cron
echo "PATH="$PATH >> bing_linux_cron
echo "DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS >> bing_linux_cron
#Setting job to execute weekdays at 8:30 AM
echo "30 08 * * 1-5 $PYTHON $SCRIPT_LOCATION -f 8 &>$LOGFILE_LOCATION" >> bing_linux_cron

#install cron
crontab bing_linux_cron

#cleaning up
rm bing_linux_cron

echo "done!"

