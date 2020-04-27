pathToPics = r'/Users/sash/mnt/zavulon_pub/cam_motion/Entrance/2020_04_13-2020_05_12'
pathToPics = r'/Users/sash/mnt/zavulon_pub/cam_motion/enrty2/2020_04_04-2020_05_03'
pathToPics = r'/share/Public/cam_motion/Entrance/2020_04_13-2020_05_12'

import os, glob
import time
from os.path import getctime
from datetime import datetime
from typing import Dict, List, Tuple

TIME_DELTA_TOLERANCE = 5 # criteria to group files

def groupPicsByTime(pathToPics=pathToPics) -> List[List[str]]:
	""" Group files by time proximity into a list
	from oldest to youngest """

	listOfFiles = glob.glob(pathToPics + r'/*.jpg') # * means all if need specific format then *.csv
	listOfFiles.sort(key=os.path.getctime)

	latestFile = listOfFiles[-1]
	latestTime = os.path.getctime(latestFile)
	# print(latestFile, latestTime)

	groupedFiles = [[listOfFiles[0], ]]

	for file in listOfFiles[1:]:
		fileName = file.split(r'/')[-1]
		# timeFormatted = datetime.fromtimestamp(getctime(file)).strftime('%Y-%m-%d %H:%M:%S')

		deltaTime = abs((getctime(groupedFiles[-1][-1]) - getctime(file)))
		if deltaTime < TIME_DELTA_TOLERANCE:
			groupedFiles[-1].append(file)
		else:
			groupedFiles.append([file,])


		# print(f'{len(groupedFiles):d} : {timeFormatted} {fileName}')

	return groupedFiles


if __name__ == '__main__':
	groupPicsByTime()