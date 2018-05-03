#!/usr/bin/python

""" Module: storageazure
	Function collection for StorageAccount related management
	
	Version: 1.0.1.0
	Last modified date: 03.05.2018.

	Usage:
	from amarettostorage import *
"""

import io
import json
import sys
import subprocess
import stat
import os
import time
import datetime


# FUNCTION Create container for files
def createContainer(containerName, storageaccountName, sasToken, timeOut = 40):
	# Check parameters
	if len(containerName) > 0 and len(storageaccountName) > 3 and len(sasToken) > 120:
		# Create command for creation
		containercmd = 'az storage container create --account-name {0} --sas-token "{1}" -n "{2}"'.format(storageaccountName, sasToken, containerName)
		# Execute command
		try:
			commandResult = subprocess.check_output(containercmd, shell=True)
			# Result is OK
			result = '{"status": "success", "result": %s}' % (commandResult)
			return result
		except:
			# Error handling
			result = '{"status": "error", "result": "Access is denied. Wrong parameter"}'
			return result
	else:
		# Wrong parameters
		result = '{"status": "error", "result": "One or more input parameter is wrong. Please check parameter list"}'
		return result


# FUNCTION Upload file to storage account
def uploadFile(fileName, fileVersion , storageaccountName, sasToken, storageKey = "none", releaseVersion = "latest", filePath = "./files/", containerName = "files", modificationLimitMin = "30"):
	# Check parameters
	if len(fileName) > 0 and len(storageaccountName) > 3 and len(sasToken) > 120 and len(fileVersion) > 0:
		# Create container for files
		containerResult = json.loads(createContainer(containerName, storageaccountName, sasToken))
		# Check container creation result
		if containerResult["status"] == "success":
			# Container has been created or exists
			# Check lastWriteTime local and in Azure
			#### Local file
			localTime = ""
			try:
				file_stats = os.stat("{0}{1}".format(filePath, fileName))
				localTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(file_stats[stat.ST_MTIME]))
			except:
				localTime = "1991-09-12 12:40:00"

					
			#### Azure Time
			azureTime = ""
			try:	
				timecmd = 'az storage blob show --account-name "{0}" --sas-token "{1}" -c "{2}" -n "{4}/{3}"'.format(storageaccountName, sasToken, containerName, fileName, releaseVersion)
				timeResult = subprocess.check_output(timecmd, shell=True)
				lastMod = json.loads(timeResult)["properties"]["lastModified"]
				azureTime = "{0} {1}".format(lastMod[:10], lastMod[11:19])
			except:
				azureTime = "1979-09-18 21:30:00"

			# Get difference
			dateDiff = json.loads(getDateDiff(localTime, azureTime))
			if (dateDiff["status"] == "success") and (int(modificationLimitMin) < int(dateDiff["result"])):
				# Move old file to its version related directory
				moveResult = json.loads(moveFile(fileName = fileName, storageaccountName = storageaccountName, sasToken = sasToken, storageKey = storageKey, currentLocation = releaseVersion, containerName = containerName))
				# Check result
				if moveResult["status"] == "success" or moveResult["status"] == "noFile":
					# Move was success or the file does not exist
				
					# Create upload command
					uploadcmd = 'az storage blob upload --account-name "{0}" --sas-token "{1}" -c "{2}" -f "{6}{3}" -n "{5}/{3}" --metadata "version={4}"'.format(storageaccountName, sasToken, containerName, fileName, fileVersion, releaseVersion, filePath)
					# Execute command
					try:
						commandResult = subprocess.check_output(uploadcmd, shell=True)
						# Result is OK
						result = '{"status": "success", "result": %s}' % (commandResult)
						return result
					except:
						# Error handling
						result = '{"status": "error", "result": "Upload failed"}'
						return result
				else:
					# Error handling
					result = '{"status": "error", "result": "An error has occurred during move old file: %s"}' % (moveResult["result"])
					return result
			else:
				result = '{"status": "notreplaced", "result": "The file in azure is fresh enough so does not need to replace."}'
				return result
		else:
			# An error has occurred during container creation
			result = '{"status": "error", "result": "Container creation failed: %s"}' % (containerResult["result"])
			return result
	else:
		# Wrong parameters
		result = '{"status": "error", "result": "One or more input parameter is wrong. Please check parameter list"}'
		return result

# FUNCTION Delete file from path
def delFile(fileName, storageaccountName, sasToken, currentLocation = "latest", containerName = "files"):
	# Check parameters
	if len(fileName) > 0 and len(storageaccountName) > 3 and len(sasToken) > 120:
		# Create delete command
		delcmd = 'az storage blob delete --account-name {0} --sas-token "{1}" -c "{2}" -n "{4}/{3}"'.format(storageaccountName, sasToken, containerName, fileName, currentLocation)
		# Execute command
		try:
			commandResult = subprocess.check_output(delcmd, shell=True)
			# Result is OK
			result = '{"status": "success", "result": %s}' % (commandResult)
			return result
		except:
			# Error handling
			result = '{"status": "error", "result": "Deletion failed or file does not exist"}'
			return result
	else:
		# Wrong parameters
		result = '{"status": "error", "result": "One or more input parameter is wrong. Please check parameter list"}'
		return result

# FUNCTION Copy file to new path
def copyFile(fileName, storageaccountName, sasToken = "none", storageKey= "none", currentLocation = "latest", containerName = "files"):
	###########################################################  
	# Check parameters
	if len(fileName) > 0 and len(storageaccountName) > 3:
		# Use SAS Token for operations
		if storageKey != "none":
			# Get file version
			getcmd = 'az storage blob metadata show --account-name {0} --account-key "{1}" -c "{2}" -n "{4}/{3}"'.format(storageaccountName, storageKey, containerName, fileName, currentLocation)
			# Init file data
			fileData = ""
			# Execute command
			try:
				fileData = json.loads(subprocess.check_output(getcmd, shell=True))
			except:
				# Error handling
				result = '{"status": "error", "result": "Get file version failed or file does not exist"}'
				return result
		
			# Check file version
			if len(fileData["version"]) <= 0:
				# Error handling - no version info
				result = '{"status": "error", "result": "No valid file version for blob: %s "}' % (fileName)
				return result

			# Create copy command
			copycmd = 'az storage blob copy start --account-name {0} --account-key "{1}" --destination-container "{2}" --source-container "{2}" --source-blob "{4}/{3}" --destination-blob "{5}/{3}"'.format(storageaccountName, storageKey, containerName, fileName, currentLocation, fileData["version"])
			# Execute command
			try:
				commandResult = subprocess.check_output(copycmd, shell=True)
				# Result is OK
				result = '{"status": "success", "result": %s, "location": "%s"}' % (commandResult, fileData["version"])
				return result
			except:
				# Error handling
				result = '{"status": "error", "result": "Copy failed"}'
				return result
		elif sasToken != "none":
			# Get file version
			getcmd = 'az storage blob metadata show --account-name {0} --sas-token "{1}" -c "{2}" -n "{4}/{3}"'.format(storageaccountName, sasToken, containerName, fileName, currentLocation)
			# Init file data
			fileData = ""
			# Execute command
			try:
				fileData = json.loads(subprocess.check_output(getcmd, shell=True))
			except:
				# Error handling
				result = '{"status": "error", "result": "Get file version failed"}'
				return result
		
			# Check file version
			if len(fileData["version"]) <= 0:
				# Error handling - no version info
				result = '{"status": "error", "result": "No valid file version for blob: %s "}' % (fileName)
				return result

			# Create copy command
			copycmd = 'az storage blob copy start --account-name {0} --sas-token "{1}" --destination-container "{2}" --source-container "{2}" --source-blob "{4}/{3}" --destination-blob "{5}/{3}"'.format(storageaccountName, sasToken, containerName, fileName, currentLocation, fileData["version"])
			# Execute command
			try:
				commandResult = subprocess.check_output(copycmd, shell=True)
				# Result is OK
				result = '{"status": "success", "result": %s}' % (commandResult)
				return result
			except:
				# Error handling
				result = '{"status": "error", "result": "Copy failed"}'
				return result

		else:
			# Sas Token and storageKey is empty
			result = '{"status": "error", "result": "Sas Token and storageKey is empty. Please check parameter list"}'
			return result

	else:
		# Wrong parameters
		result = '{"status": "error", "result": "One or more input parameter is wrong. Please check parameter list"}'
		return result


# FUNCTION Move file from from current location to right releaee versio 
def moveFile(fileName, storageaccountName, sasToken, storageKey= "none", currentLocation = "latest", containerName = "files"):
	# Check parameters
	if len(fileName) > 0 and len(storageaccountName) > 3 and len(sasToken) > 120:
		# Check whether the file exist or not
		## Create related command
		existcmd = 'az storage blob exists --account-name {0} --sas-token "{1}" -c "{2}" -n "{4}/{3}"'.format(storageaccountName, sasToken, containerName, fileName, currentLocation)
		# init command Result
		isExists = False
		# Execute command
		try:
			commandResult = subprocess.check_output(existcmd, shell=True)
			isExists = json.loads(commandResult)["exists"]
		except:
			# Error handling
			errorMessage = "Issue has been detected"
		# If the file exists start copy then deletion
		if isExists:
			# Copy file to right location
			copyResult = json.loads(copyFile(fileName = fileName, storageaccountName = storageaccountName, sasToken = sasToken, storageKey = storageKey, currentLocation = currentLocation, containerName = containerName))
			# Check copyresult
			if copyResult["status"] == "success":
				# Copy was success
				# Delete file from original location
				deleteResult = json.loads(delFile(fileName, storageaccountName, sasToken, currentLocation, containerName))
				# Check delete result
				if deleteResult["status"] == "success":
					# Result is OK
					result = '{"status": "success", "result": "%s has been successfully moved to %s directory"}' % (fileName, copyResult["location"])
					return result
				else:
					# An error has occurred during deletion
					result = '{"status": "error", "result": "An error has occurred during delete %s file: %s"}' % (fileName, deleteResult["result"])	
					return result
			else:
				# An error has occurred during copy
				result = '{"status": "error", "result": "An error has occurred during copy %s file: %s"}' % (fileName, copyResult["result"])
				return result
		else:
			# The file does not exist
			result = '{"status": "noFile", "result": "The %s file does not exist"}' % (fileName)
			return result
	else:
		# Wrong parameters
		result = '{"status": "error", "result": "One or more input parameter is wrong. Please check parameter list"}'
		return result	

# FUNCTION Move all files to their right location
def moveAllFiles(storageaccountName, sasToken, storageKey = "none", currentLocation = "latest", containerName = "files"):
	# Check parameters
	if len(storageaccountName) > 3 and len(sasToken) > 120:
		# List all files in current location
		## Create command
		listcmd = 'az storage blob list --account-name {0} --sas-token "{1}" -c "{2}" --prefix "{3}/"'.format(storageaccountName, sasToken, containerName, currentLocation)
		# Init listResult
		listResult = ""
		# Execute command
		try:
			listResult = json.loads(subprocess.check_output(listcmd, shell=True))
		except:
			# Error handling
			result = '{"status": "error", "result": "There is no any file in the %s directory"}' % (currentLocation)
			return result
		
		# Check number of items
		if len(listResult) > 0:
			# init move counter
			moved = 0
			# Seek on items
			for file in listResult:
				# Convert file to fileName
				fileName = file["name"].split('/')[1]
				# Move current file to its right location
				moveResult = json.loads(moveFile(fileName = fileName, storageaccountName = storageaccountName, sasToken = sasToken, storageKey = storageKey, currentLocation = currentLocation, containerName = containerName))
				# Check result
				if moveResult["status"] == "success" or moveResult["status"] == "noFile":
					moved += 1

			# Check batch move result
			if len(listResult) == moved:
				# All are moved
				result = '{"status": "success", "result": "%s files have been successfully moved to their version related directory"}' % (moved)
				return result
			else:
				# Error handling
				result = '{"status": "error", "result": "An error has occurred. %s of %s files have been moved sucessfully. Please check the others"}' % (moved, len(listResult))	
				return result

		else:
			# Error handling
			result = '{"status": "error", "result": "No files in the %s directory"}' % (currentLocation)
			return result
		

	else:
		# Wrong parameters
		result = '{"status": "error", "result": "One or more input parameter is wrong. Please check parameter list"}'
		return result	
	
# FUNCTION Upload file to storage account
def uploadAllFiles(fileVersion , storageaccountName, sasToken, storageKey = "none", releaseVersion = "latest", filePath = "./files/", containerName = "files", modificationLimitMin = "30"):
	# Import packages
	import time
	from os import listdir
	from os.path import isfile, join
	# Check parameters
	if len(storageaccountName) > 3 and len(sasToken) > 120 and len(fileVersion) > 0:
		# List all files from path
		listFiles = [f for f in listdir(filePath) if isfile(join(filePath, f))]
		# Check number of items
		if len(listFiles) > 0:
			# init uploaded counter
			uploaded = 0
			# init newer counter
			notreplaced = 0
			# Seek on items
			for fileName in listFiles:
				# Upload current file to Azure
				uploadResult = json.loads(uploadFile(fileName = fileName, fileVersion = fileVersion, storageaccountName = storageaccountName, sasToken = sasToken, storageKey = storageKey, releaseVersion = releaseVersion, filePath = filePath, containerName = containerName, modificationLimitMin = modificationLimitMin))
				# Check result
				if uploadResult["status"] == "success" or uploadResult["status"] == "notreplaced":
					uploaded += 1
					if uploadResult["status"] == "notreplaced":
						notreplaced += 1	
				# Delay: 1 sec
				time.sleep(1) 
			# Check batch move result
			if len(listFiles) == uploaded:
				# All are moved
				# Generate newer value
				from datetime import timedelta  
				from datetime import datetime
				newer = datetime.now() - timedelta(minutes=int(modificationLimitMin))
				# Generate result
				result = '{"status": "success", "result": "%s files have been successfully uploaded to %s storage account.( %s files were not uploaded to Azure because they are newer than %s)"}' % (uploaded, storageaccountName, notreplaced, newer)
				return result
			else:
				# Error handling
				result = '{"status": "error", "result": "An error has occurred. %s of %s files have been uploaded sucessfully. Please check the others"}' % (uploaded, len(listFiles))	
				return result

		else:
			# Error handling
			result = '{"status": "error", "result": "No files in the directory: %s"}' % (filePath)
			return result
		
	else:
		# Wrong parameters
		result = '{"status": "error", "result": "One or more input parameter is wrong. Please check parameter list"}'
		return result

	
# FUNCTION Get difference between two dates
def getDateDiff(localFileDateTime, azureFileDateTime):
	from datetime import datetime
	azureDate = ""
	localDate = ""
	# Convert
	try:
		azureDate = datetime.strptime(azureFileDateTime, "%Y-%m-%d %H:%M:%S")
		localDate = datetime.strptime(localFileDateTime, "%Y-%m-%d %H:%M:%S")
	except:
		return '{"status":"error", "result":"wrong input parameters"}'
		# Calculate difference
	try:
		diff = (localDate - azureDate)
		# Check in days
		inDays = diff.days
		if  inDays >= 0:
			# Check in minutes
			inMinutes = (diff.seconds / 60) + (inDays * 3600)
			return '{"status":"success", "result":"%s"}' % (inMinutes)
		else:
			return '{"status":"success", "result":"%s"}' % (inDays)
	except:
		return '{"status":"error", "result":"Datetime parsing error"}'

