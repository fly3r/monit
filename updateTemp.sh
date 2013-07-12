#!/bin/bash
# Call this script to update json feed before send to Xively
# feedUpdate.json
# sh updateJSON <filename>

#./updateJSON feedUpdate.json

cpuTemp0=$(cat /sys/class/thermal/thermal_zone0/temp)
cpuTemp1=$(($cpuTemp0/1000)) cpuTemp2=$(($cpuTemp0/100))
cpuTempM=$(($cpuTemp2 % $cpuTemp1))

cpuTempC=$cpuTemp1.$cpuTempM
echo ">> CPU Temp: "$cpuTempC "C <<"
sed -i '5s/.*/"current_value":"'$cpuTempC'"},/' feedUpdate.json

cpuLoad=$(cat /proc/loadavg | awk '{print $1}')
echo ">> CPU Load: "$cpuLoad" <<"
sed -i '7s/.*/"current_value":"'$cpuLoad'"},/' feedUpdate.json

ir0_C=$(tail -2 optrisCT_log.txt | head -1 | awk '{print $5}')
echo ">> IR0: "$ir0_C" <<"
sed -i '9s/.*/"current_value":"'$ir0_C'"},/' feedUpdate.json

ir1_C=$(tail -2 optrisCT_log.txt | head -1 | awk '{print $7}')
echo ">> IR1: "$ir1_C" <<"
sed -i '11s/.*/"current_value":"'$ir1_C'"}/' feedUpdate.json


curl -k --request PUT --data-binary @feedUpdate.json --header "X-ApiKey:MnfHud2lfTtbE6JFIT6R9ObxyWFQUh8Z8UXjZCYOAvLmuDeg" --verbose https://api.xively.com/v2/feeds/2089212838
