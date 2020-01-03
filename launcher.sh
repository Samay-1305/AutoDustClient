#!/bin/sh
# launcher.sh

cd ~/Projects/AutoDust/

until sudo python3 AutoDust.py > AutoDustLog.txt
    do
        echo "Program Crashed Unexpectedly... Restarting"
done

cd ~
