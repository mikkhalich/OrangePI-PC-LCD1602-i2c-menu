1. Encoder connection pins are set in the file "encoder.py"
 default connection:
 	enc  | Orangepi PC
	-----|------------ 
	VCC  | +3.3v
	GND  | gnd
	clk  | pin 1
	dt   | pin 0
	btn  | pin 3

2. Electrical circuit

 - Encoder pins (clk, dt, btn) connected to OrngePi pins (0,1,3) in series with 1k resistor
 - Encoder pins pulled to ground by 10k resistors
 - Do not forget about capacitors for noise suppression of the encoder


2. Lcd1602 connection:
 default connection:
	LCD | Orangepi PC
	----|------------ 
	VCC | +3.3v
	GND | gnd
	SDA | pin 3
	SCL | pin 5
	
 default parametrs:	
	I2C_ADDR  = 0x27
	bus = smbus.SMBus(0)  # Rev 1 Pi uses 0 and orangepi_pc pin 3,5

Sofrware

1. unpack the contents into a folder:
'/home/pi/'
so that the "menu_lcd1602.py", was on the addres
"/home/pi/RetroPie/lcd/sources/menu_lcd1602.py"

2. sudo ./home/pi/RetroPie/lcd/sources/install.sh

3. enjoy

===================================================================
https://www.sites.google.com/site/orangepizero/logitech-media-server/lcd-i2c

i2c FOR ORANGE PI ZERO (or ORANGE PI ONE) WITH ARMBIAN in the Jessie flavor

1. declare the modules with nano in "/etc/modules" adding the line 
i2c-bcm2708 
i2c-dev
Then reboot

3. add gpio module: 
sudo modprobe gpio-sunxi

4. add python smbus 
sudo apt-get install python-smbus

5. install tool for i2c: 
sudo apt-get install i2c-tools

6. read address of I2C LCD 
sudo i2cdetect -y 0

0 - bus number

you will get something like that (use -y 1 depending on your card):

root@orangepizero:/mnt/dlink/Raspberry/Python# sudo i2cdetect -y 0

     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f

00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3f 
40: -- -- -- -- -- -- -- -- UU -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                         

Please note if the address is not x3f then you have to pass your address in parameter to the app. using -l parameter

7. install python installer package 
sudo apt-get install python-pip

8. add setupools for xenial (not required for Debian) 
sudo apt-get install python-setuptools
