#!/bin/bash

sudo cp ./menu_lcd1602.service /etc/systemd/system/menu_lcd1602.service
sudo chmod +x  /etc/systemd/system/menu_lcd1602.service

sudo systemctl enable menu_lcd1602
sudo systemctl start menu_lcd1602
