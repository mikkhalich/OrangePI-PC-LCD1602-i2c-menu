#!/bin/bash
cp ./menu_startup.sh /etc/init.d/menu_startup.sh
sudo chmod +x /etc/init.d/menu_startup.sh
sudo insserv -v /etc/init.d/menu_startup.sh
