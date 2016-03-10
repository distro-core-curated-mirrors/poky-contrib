#!/bin/sh

stick1_m='537133064'
stick2_m='536875016'
stick3_m='266248'
stick4_m='537137152'
all_sticks_m='537137160'

j=1

get_stick_serial_no(){
  serial=''
  for i in $(ls /dev/sd? | grep -v /dev/sda)                                                                                                        
  do                                                                                                                                                
    serial=$(udevadm info --attribute-walk --name=${i} | grep serial | grep -v : | awk -F'"' '{print $2}'):$serial #pentru a detecta serial-ul usbstick-ului
  done  
echo $serial
}



##################### MAIN #####################
w_dir="/root/USB_SW/config_files"

j=1
:>${w_dir}/stick_serials.cfg

#${w_dir}/control $all_sticks_m
echo "$all_sticks_m" > ${w_dir}/last_word_sent 
python SW_interface.py  
#kill -1 `ps aux | grep "/root/USB_SW/sw_daemon.py" | grep -v grep | awk '{print $2}'`

sleep 15

for i in $stick1_m $stick2_m $stick3_m $stick4_m 
do
  echo "$i" > ${w_dir}/last_word_sent
  #kill -1 `ps aux | grep "/root/USB_SW/sw_daemon.py" | grep -v grep | awk '{print $2}'`
  python SW_interface.py  
  sleep 15
  serial=$(get_stick_serial_no)
  echo "stick${j}:${serial}" >> ${w_dir}/stick_serials.cfg 
  j=$(($j+1))
done

echo "0" > ${w_dir}/last_word_sent
#kill -1 `ps aux | grep "/root/USB_SW/sw_daemon.py" | grep -v grep | awk '{print $2}'`

python SW_interface.py  
