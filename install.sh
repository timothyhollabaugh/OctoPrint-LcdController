/etc/init.d/lcd stop
sudo rm /etc/init.d/lcd
sleep 1
sudo update-rc.d lcd remove
sudo cp lcd /etc/init.d
sudo update-rc.d lcd defaults