#!/usr/bin/python2

import os
import sys
import time

import lcd_i2c
import encoder

diplayRows = 2       # lcd display 's rows count  
curMenuItem = [0,0]  # current menu position (<main menu item number>, <sub menu item number>)
subMenuFlag = False

dispShowInfoState = False
infoStateStr = ""
menuList = []

redrawFlag = True

# runnig string 
shiftCnt = 0
shiftMax = 64
shiftForward = True
shiftTimeInterval = 0.5
shiftStartTime = 0

def shiftText (strValue, strLen):
	# shift strValue
	# Returns a shifted string of <strLen> characters
	
	global shiftCnt
	global shiftForward
	
	if len (strValue)>strLen:
		tmpInfoState = strValue[shiftCnt:shiftCnt+strLen]
		if shiftForward:
			if len(strValue)> (shiftCnt + strLen):
				shiftCnt +=1
			else:
				shiftForward = False
		else:
			if shiftCnt>0:
				shiftCnt -=1
			else:
				shiftForward = True
	else:
		tmpInfoState = strValue
		
	return tmpInfoState

def drawMenu (menuList, infoRow2=""):
	# drawMenu proc
	global redrawFlag
	global curMenuItem
	global diplayRows
	global shiftCnt
	global shiftForward
	
	if redrawFlag:
		#  need redraw ?
		
		redrawFlag = False
		
		# length of menu list
		if subMenuFlag:
			tmpLen = len(menuList[curMenuItem[0]][1]) # lenght of submenu list
		else:
			tmpLen = len(menuList) # lenght of main menu list
			
		if tmpLen > 0:
			# Slice display menu items
			
			if subMenuFlag:
				tmpList = menuList[curMenuItem[0]][1]
				tmpList = tmpList[curMenuItem[1]:curMenuItem[1]+diplayRows]
			else:
				tmpList = [x[0] for x in menuList][curMenuItem[1]: ]
				tmpList = tmpList[:diplayRows]
			
			rowCnt = 0 # lcd display row counter
			
			# info mode, display mode command result
			if dispShowInfoState:
				
				LcdRow = '[' +shiftText(tmpList[0], 12)+ ']'
				LcdRow = os.path.basename(LcdRow)
				LcdRow = LcdRow[0:13]
				LcdRow = LcdRow.ljust(13) + ' ' + str(curMenuItem[1])
				lcd_i2c.lcd_string(LcdRow, lcd_i2c.LCD_LINE_1)

				tmpInfoState = shiftText(infoStateStr, 15)
					
				lcd_i2c.lcd_string(tmpInfoState, lcd_i2c.LCD_LINE_2)	
			else:
			# menu mode
				for ii in tmpList:
					
					if subMenuFlag:
						LcdRow = ii
					else:
						LcdRow = os.path.basename(ii)[2:]
					
					if rowCnt % 2 == 0 :
						# even lines of the display (0,2,4...)
						if curMenuItem[1] == curMenuItem[1] + rowCnt:	
							LcdRow = shiftText(LcdRow, 10)	
							LcdRow = '[' + LcdRow + ']'
							
						LcdRow = LcdRow.ljust(13)	
							
						LcdRow = LcdRow + ' ' + str(tmpLen)
						lcd_i2c.lcd_string(LcdRow, lcd_i2c.LCD_LINE_1)
					else:
						# odd lines of the display (0,2,4...)
						LcdRow = LcdRow[0:12]
						LcdRow = LcdRow.ljust(13)
						
						LcdRow = LcdRow + ' ' + str(curMenuItem[1]+1)
						lcd_i2c.lcd_string(LcdRow, lcd_i2c.LCD_LINE_2)
					rowCnt +=1
					
				# if the second line of the display is empty	
				if rowCnt<2:
					lcd_i2c.lcd_string('              ' + str(curMenuItem[1]+1), lcd_i2c.LCD_LINE_2)
	
def encUp(value):
	#callback encoder Up callback proc
	global curMenuItem
	global redrawFlag
	global subMenuFlag
	global shiftCnt
	global globalshiftForward
	
	# running line 
	shiftCnt = 0
	globalshiftForward = True
	
	# selection of the current menu item
	if curMenuItem[1] > 0:
		curMenuItem[1] -= 1
		redrawFlag= True
		
def encDown(value):
	#callback encoder down callback proc
	global curMenuItem
	global redrawFlag
	global subMenuFlag
	global shiftCnt
	global globalshiftForward
	
	# running line 
	shiftCnt = 0
	globalshiftForward = True	
	
	# selection of the current menu item
	if subMenuFlag:
		#for sub menu
		if curMenuItem[1] < len(menuList[curMenuItem[0]][1]) -1:
			curMenuItem[1] += 1
			redrawFlag= True

	else:	
		#for main menu
		if curMenuItem[1] < len(menuList) -1:
			curMenuItem[1] += 1
			redrawFlag= True
				
		
def shortClick():
	#encoder short Click callback proc
	global curMenuItem
	global infoStateStr
	global dispShowInfoState
	global redrawFlag
	global subMenuFlag
	global menuList
	
	redrawFlag= True

	if subMenuFlag == False:
		#goto submenu	
		curMenuItem[0] = curMenuItem[1]
		curMenuItem[1] = 0
		subMenuFlag = True
		
	elif subMenuFlag and dispShowInfoState == False: 
		# run script and show runnig string in lcd2 row
		if curMenuItem[1] > 0:
			tmpList = menuList[curMenuItem[0]]
			tmpScriptPatch = os.path.join	(tmpList[0], tmpList[1][curMenuItem[1]])
			
			dispShowInfoState = True
			try:
				scriptResult = getConsoleOut(tmpScriptPatch)
				if scriptResult[1]:
					infoStateStr = scriptResult[0].rstrip()
					if len(infoStateStr)>0:
						infoStateStr = ' '.join(infoStateStr.split())
						infoStateStr = infoStateStr [:shiftMax] # max length of info string 
					else:
					# if the script output is empty
						infoStateStr = 'Ok'
					
			except:
				# if an error occurred running the script
				infoStateStr = 'Error!' 
				

		elif curMenuItem[1] == 0:
		# if select '..' menu item
			longClick()
		
	elif subMenuFlag and dispShowInfoState == True: 
		# show submenu
		dispShowInfoState = False

def longClick():
	# encoder long click callback proc
	
	global curMenuItem
	global redrawFlag
	global subMenuFlag
	global dispShowInfoState
	
	redrawFlag= True
	
	if subMenuFlag  and dispShowInfoState == False: 
		#goto submenu	
		curMenuItem[1] = curMenuItem[0]
		curMenuItem[0] = 0
		subMenuFlag = False
		
	elif subMenuFlag  and dispShowInfoState == True: 
		dispShowInfoState = False

def getConsoleOut(comList):
	# return console output and run result
	# comList = ["ls","-l"]
	from subprocess import check_output, CalledProcessError, STDOUT
	try:
		output = check_output (comList, stderr = STDOUT).decode()
		success = True
	except CalledProcessError as e:
		output = e.output.decode()
		success = False
	
	return [output, success]

def getDirsAndFiles (patch):
	# return Dir's list (dirs begin in '__') and subfiles in dirs
	
	
	tmpPath = tmpPatch = os.path.normpath(patch)
	resultList	 = []
	
	tmpDirlist = next(os.walk(tmpPath))[1]
	dirList = []
	
	#list og subdirs starting with "__"
	for ii in tmpDirlist:
		if len(ii)>2 and ii[0:2] == '__':
			dirList.append(ii)
	
	# add subdir files list			
	for ii in dirList:
		tmpPatch = os.path.join	(patch, ii)
		tmpFilesList = next(os.walk(tmpPatch))[2]
		
		# add '[..]' menu item
		#tmpPatch.sort()
		tmpList = [['..'].extend (tmpPatch)]
		tmpFilesList.insert(0, '..')
		tmpList = [tmpPatch]
		tmpList.append(tmpFilesList)
		resultList.append(tmpList)
		
	return resultList


def main():
	global menuList
	global dispShowInfoState
	global shiftTimeInterval
	global shiftStartTime
	global redrawFlag
	
	menuList = getDirsAndFiles (".")
	
	lcd_i2c.lcd_init()

	while True:
		time.sleep (0.005)
		drawMenu (menuList, "")
		encoder.getEncoderState(encUp, encDown, shortClick, longClick)
		
		# runnung string
		#if 	dispShowInfoState:
		if (time.time() - shiftStartTime) > shiftTimeInterval:
			shiftStartTime = time.time()
			redrawFlag = True
				
if __name__ == '__main__':
	main()		





