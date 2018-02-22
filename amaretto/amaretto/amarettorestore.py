#!/usr/bin/python

""" Module: amaretto restore
    Function collection for Restore VMs
	
	Version: 1.2.0.0
	Last modified date: 22.02.2018.

	Usage:
	from amarettorestore import *
"""

import io
import json
import sys
import subprocess

# FUNCTION Put message to stdout
def messenger(inputString):
	import time
	# Check input
	if len(inputString) > 0:
		# Return with datetime and message
		return sys.stdout.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + inputString + '\n')
	else:
		return False

# FUNCTION Get OS Disk name from backup file - Unmanaged disk
def getOSDiskVhdInfo(filePath):
	# Open input file
	with open(filePath) as f:
		s = f.read()
	
	# initial value for vhdName
	vhdName = "none"
	# Deploy type config.json or AzureDeploy.json
	deployType = 0
	# Load resources from input file
	resourcesCount = 0
	try:
		## Config.json related structure
		resourcesCount = len(json.loads(s)["properties.storageProfile"])
		# Deploy type is config - 1
		deployType = 1
	except:
		## Azuredeploy.json related structure
		resourcesCount = len(json.loads(s)["resources"])
		# Deploy type is azuredeploy - 2
		deployType = 2

	# Check resource count ans deployment type
	if int(resourcesCount != 0) and (deployType == 1):
		# Deploy type is config
		# Get vhd uri
		uri = json.loads(s)["properties.storageProfile"]["osDisk"]["vhd"]["uri"]
		# Get VHD name
		vhdName = uri.split("/")[len(uri.split("/")) - 1]
	elif int(resourcesCount != 0) and (deployType == 2):
		# Deploy type is azuredeploy
		# Set indicator to -1
		resourceIndex = -1
		# Seek on resources in input file
		for r in range(resourcesCount):
			# Work on virtualMachines types only
			if "virtualMachines" in json.loads(s)["resources"][r]["type"]:
				# Set resource index to current index
				resourceIndex = r
				# Get vhd uri
				uri = json.loads(s)["resources"][resourceIndex]["properties"]["storageProfile"]["osDisk"]["vhd"]["uri"]
				# Get VHD name
				vhdName = uri.split("/")[len(uri.split("/")) - 1]

			
	# Check vhdName length and initial value
	if (len(vhdName) > 0) and (vhdName != "none"):
		# It is not empty
		## Return with result
		return '{"name": "%s", "uri": "%s"}' % (vhdName, uri)
	else:
		# It is empty
		## Return with error
		return {"name": "none", "uri": "error"}

# FUNCTION Get Data Disk name from backup files
def getDataDiskVhdInfo(filePath):
	# Open input file
	with open(filePath) as f:
		s = f.read()
	# Initial value for vhdName
	vhdName = "none"
	# Initial value for datadisk count
	diskCount = 0
	# Deploy type config.json or AzureDeploy.json
	deployType = 0
	# Load resources from input file
	resourcesCount = 0
	try:
		## Config.json related structure
		resourcesCount = len(json.loads(s)["properties.storageProfile"])
		# Deploy type is config - 1
		deployType = 1
	except:
		## Azuredeploy.json related structure
		resourcesCount = len(json.loads(s)["resources"])
		# Deploy type is azuredeploy - 2
		deployType = 2

	# Check resource count ans deployment type
	if int(resourcesCount != 0) and (deployType == 1):
		# Deploy type is config
		# Set vhdname to empty string
		vhdName = '{"dataDisks": ['
		# Get datadisk count from file
		diskCount = len(json.loads(s)["properties.storageProfile"]["dataDisks"])
		# Seek on datadisks part
		for i in range(diskCount):
			# Get current disk uri
			uri = json.loads(s)["properties.storageProfile"]["dataDisks"][i]["vhd"]["uri"]
			# Get current disk name
			name = uri.split("/")[len(uri.split("/")) - 1]
			# Get current disk lun
			lun = json.loads(s)["properties.storageProfile"]["dataDisks"][i]["lun"]
			# Append the current disk name to vhdname list
			## 0th record is different
			if i == 0:
				# No comma before the section
				vhdName = vhdName + '{"lun": %s, "name": "%s", "uri": "%s"}' % (lun, name, uri)
			else:
				# Puts a comma before the section
				vhdName = vhdName + ', {"lun": %s, "name": "%s", "uri": "%s"}' % (lun, name, uri)
		# Close json
		vhdName = vhdName + "]}"
	elif int(resourcesCount != 0) and (deployType == 2):
		# Deploy type is azuredeploy
		# Set indicator to -1
		resourceIndex = -1
		# Seek on resources in input file
		for r in range(resourcesCount):
			# Work on virtualMachines types only
			if "virtualMachines" in json.loads(s)["resources"][r]["type"]:
				# Set resource index to current index
				resourceIndex = r
				# Set vhdname to empty string
				vhdName = '{"dataDisks": ['
				# Get datadisk count from file
				diskCount = len(json.loads(s)["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"])
				# Seek on datadisks part
				for i in range(diskCount):
					# Get current disk uri
					uri = json.loads(s)["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"][i]["vhd"]["uri"]
					# Get current disk name
					name = uri.split("/")[len(uri.split("/")) - 1]
					# Get current disk lun
					lun = json.loads(s)["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"][i]["lun"]
					# Append the current disk name to vhdname list
					## 0th record is different
					if i == 0:
						# No comma before the section
						vhdName = vhdName + '{"lun": %s, "name": "%s", "uri": "%s"}' % (lun, name, uri)
					else:
						# Puts a comma before the section
						vhdName = vhdName + ', {"lun": %s, "name": "%s", "uri": "%s"}' % (lun, name, uri)
				# Close json
				vhdName = vhdName + "]}"
			
	# Check vhdName length and initial value
	if (len(vhdName) > diskCount) and (vhdName != "none"):
		# It is not empty
		## Return with result
		return vhdName
	else:
		# It is empty
		## Return with error
		return '{"dataDisk": [ {"lun": 0, "name": "none", "uri": "error"}]}'


# FUNCTION gives back storage uri according to Azure cloud name
def storageUriFromCloud(cloudName = "AzureGermanCloud"):
	# Check whether this is MCD
	if cloudName == "AzureGermanCloud":
		# If MCD it gives back the right uri
		return "blob.core.cloudapi.de"
	else:
		# If MCI it gives back the right uri
		return "blob.core.windows.net"

# FUNCTION get datadisk information for required lun
def setDataDisk(filename, lun, VHDName, storageAccountName, cloudName = "AzureGermanCloud"):
	# Concatenate vhd uri
	vhdStorageUri = "https://" + storageAccountName + "." + storageUriFromCloud(cloudName) + "/vhds/" + VHDName + ".vhd"
	# Open file for read
	with open(filename, "r") as jsonFile:
		data = json.load(jsonFile)
	# Get resources count    
	resourcesCount = len(data["resources"])
	# Set resource index
	resourceIndex = -1
	# Seek on resource list (file)
	for r in range(resourcesCount):
		# It manages only virtualMachines objetc
		if "virtualMachines" in data["resources"][r]["type"]:
			# Set resource index value for the current index
			resourceIndex = r
			   
	# Set disk count from file
	diskCount = len(json.loads(s)["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"])
	# Seek on data disk count
	for i in range(diskCount):
		# Manages the data which related the required lun
		if  int(data["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"][i]["lun"]) == int(lun):
			# Put old value to a temp variable
			tmpName = data["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"][i]["name"]
			# Set new value
			data["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"][i]["name"] = VHDName

			# Put old uri to temp variable
			tmpUri = data["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"][i]["vhd"]["uri"]
			# Set new value
			data["resources"][resourceIndex]["properties"]["storageProfile"]["dataDisks"][i]["vhd"]["uri"] = vhdStorageUri

	# Write back the changed content, if found in the file
	with open(filename, 'w') as jsonFile:
		json.dump(data, jsonFile)

# FUNCTION get osdisk information
def setOSDisk(filename, VHDName, storageAccountName, cloudName = "AzureGermanCloud"):
	# Concatenate vhd uri
	vhdStorageUri = "https://" + storageAccountName + "." + storageUriFromCloud(cloudName) + "/vhds/" + VHDName + ".vhd"
	# Open file for read
	with open(filename, "r") as jsonFile:
		data = json.load(jsonFile)
	# Get resources count     
	resourcesCount = len(data["resources"])
	# Set resource index
	resourceIndex = -1
	# Seek on resource list (file)
	for r in range(resourcesCount):
		# It manages only virtualMachines objetc
		if "virtualMachines" in data["resources"][r]["type"]:
			# Set resource index value for the current index
			resourceIndex = r
		
	# Set os disk uri by resource index from file
	uri = json.loads(s)["resources"][resourceIndex]["properties"]["storageProfile"]["osDisk"]["vhd"]["uri"]
	# Put old name ro temp variable  
	tmpName = data["resources"][resourceIndex]["properties"]["storageProfile"]["osDisk"]["name"]
	# Set new value
	data["resources"][resourceIndex]["properties"]["storageProfile"]["osDisk"]["name"] = VHDName

	# Put old uri to temp variable
	tmpUri = data["resources"][resourceIndex]["properties"]["storageProfile"]["osDisk"]["vhd"]["uri"]
	# Set new value
	data["resources"][resourceIndex]["properties"]["storageProfile"]["osDisk"]["vhd"]["uri"] = vhdStorageUri

	# Write back the changed content, if found in the file
	with open(filename, 'w') as jsonFile:
		json.dump(data, jsonFile)


# FUNCTION Get deploy filename
def getFileName(storageAccount, secretKey, continer):
	# Check if config.json exists or not
	command = 'az storage blob list -c {0} --account-name {1}  --account-key {2}  --prefix config'.format(continer, storageAccount, secretKey)
	# Execute command for config.json
	result = subprocess.check_output(command, shell=True)
	# Try to format the result in JSON
	try:
		# Create result
		result = '{"name": "%s", "type": "config.json"}' % (json.loads(result)[0]["name"])
		# If success it give back as result
		return result 
	except:
		# Check if azuredeploy.json exists or not
		command = 'az storage blob list -c {0} --account-name {1}  --account-key {2}  --prefix azuredeploy'.format(continer, storageAccount, secretKey)
		# Execute command for azuredeploy.json
		result = subprocess.check_output(command, shell=True)
		# Try to format the result in JSON
		try:
			# Create result as json
			result = '{"name": "%s", "type": "azuredeploy.json"}' % (json.loads(result)[0]["name"])
			# If success it give back as result
			return result 
		except:
			#If it is not valid json result it gives back an error
			result = '{"name": "null", "type": "error"}'
			return result

# FUNCTION Download config file for restore
def downloadDeployFile(sourceStorageAccount, sourceSecretKey, sourceContainer, sourceFile, targetFile):
	# Create download command
	downloadCommand = "az storage blob download -c {0} --account-name {1}  --account-key '{2}' -n {3} -f {4}".format(sourceContainer, sourceStorageAccount, sourceSecretKey, sourceFile, targetFile)
	try:
		# Execute download command
		downloadResult = subprocess.check_output(downloadCommand, shell=True)
		if json.loads(downloadResult)["name"] == sourceFile:
			# File has been downloaded
			return True
		else:
			# Issue during download
			return False
	except:
		# Something went wrong
		return False



# FUNCTION Convert file if necessary
def convertFiletoText(fileName):
	import os
	# Check if input file exists
	if  os.path.isfile(fileName):
		# if exists
		## Try to open as json jile 
		try:
			with open(fileName) as json_data:
				d = json.loads(json_data)
				json_data.close()
			return True
		# if it is not valid JSON file it starts to convert it
		except:
			## try to open to read
			try:
				with io.open(fileName,'r',encoding='utf_16_le') as f:
					# Put content to a variable
					content = f.read()
				# Remove unnecessary characters from end of file
				content = content.rstrip('\x00')
		
				# process UTF-8 text
				with io.open(fileName,'w',encoding='utf8') as f:
					# Write back content to file
					f.write(content)
				# open to test the converted file
				encodedfile = open(fileName,'r')
				encodedcontent = json.loads(encodedfile.read())
				return True
			except:
				return False
		else:
			return False

# FUNCTION Deallocate vm
def deallocateVM(vmName, resourceGroup, await = True):
	# Check parameters
	if len(vmName) > 3 and len(resourceGroup) > 3:
		# vmName is OK
		# Check VM in Azure
		command = "az vm show --resource-group {0} --name {1}".format(resourceGroup, vmName)
		# Execute command
		result = subprocess.check_output(command, shell=True)
		# Check result
		if len(result) == 0:
			# VM does not exist => deallocated
			return True
		# If VM exists start deallocate activities
		# Check await parameter
		if await:
			# If wait for full stopping
			# Create deallocation  command with wait
			command = "az vm deallocate --resource-group {0} --name {1}".format(resourceGroup, vmName)
			try:
				# Execute command
				result = subprocess.check_output(command, shell=True)

				# Check result
				if json.loads(result)["status"] == 'Succeeded':
					# Succeeded
					return True
				else:
					# Not succeeded
					return False
			except:
				# Not succeeded
				return False
		else:
			# If no-wait for full stopping
			# Create deallocation  command with no-wait
			command = "az vm deallocate --resource-group {0} --name {1} --no-wait".format(resourceGroup, vmName)
			try:
				# Execute command
				result = subprocess.check_output(command, shell=True)
				return True
			except:
				return False


# FUNCTION Delete vm object
def deleteVmObject(vmName, resourceGroup, await = True):
	# Check parameters
	if len(vmName) > 3 and len(resourceGroup) > 3:
		# vmName is OK
		# Check VM in Azure
		command = "az vm show --resource-group {0} --name {1}".format(resourceGroup, vmName)
		# Execute command
		result = subprocess.check_output(command, shell=True)
		# Check result
		if len(result) == 0:
			# VM does not exist => deallocated
			return True
		# If VM exists start delete activities
		#Check await parameter
		if await:
			# If wait for deletion
			# Create delete command with wait
			command = "az vm delete --resource-group {0} --name {1} --yes".format(resourceGroup, vmName)
			try:
				# Execute command
				result = subprocess.check_output(command, shell=True)

				# Check result
				if json.loads(result)["status"] == 'Succeeded':
					# Succeeded
					return True
				else:
					# Not succeeded
					return False
			except:
				# Not succeeded
				return False
		else:
			# If no-wait for deletion
			# Create delete command with no-wait
			command = "az vm delete --resource-group {0} --name {1} --no-wait --yes".format(resourceGroup, vmName)
			try:
				# Execute command
				result = subprocess.check_output(command, shell=True)
				return True
			except:
				return False

# FUNCTION Delete vhd file
def deleteUnmanagedDisk(vhdName, storageAccount, secretKey, container):
	# Set init parameters
	ifExists = False
	# Check existing item
	# Create show command
	showCommand = "az storage blob show -c '{0}' --account-key '{1}' --account-name '{2}' -n '{3}'".format(container, secretKey, storageAccount, vhdName)
	# Execute show command
	showResult = subprocess.check_output(showCommand, shell=True)
	# Check result
	try:
		# Convert to json
		sResult = json.loads(showResult)
		# compare result
		if sResult["name"] == vhdName:
			# Set variable to True
			ifExists = True
	except:
		# Error at checking
		return False

	#if exists start Deletion
	if ifExists:
		 # Start deletion
		try:
			# Create delete command
			deleteCommand = "az storage blob delete -c '{0}' --account-key '{1}' --account-name '{2}' -n '{3}'".format(container, secretKey, storageAccount, vhdName)
			# Execute delete command
			deleteResult = subprocess.check_output(deleteCommand, shell=True)
			# Check result"
			if  len(json.loads(deleteResult)) == 1:
				# Deleted
				return True
		except:
			# Error at deletion
			return False
	else:
		# Does not exis
		return False


# FUNCTION Delete managed disk
def deleteManagedDisk(diskName, resourceGroup):
	# Collect information
	managedDiskName = ""
	managedDiskSize = ""
	managedDiskTags = ""
	# init result
	result = ""
	# Create manage disk show command
	showCommand = 'az disk show -n "{0}" -g "{1}" --verbose'.format(diskName, resourceGroup)
	# Execute command
	showResult = subprocess.check_output(showCommand, shell=True)
	# Check result before deletion
	try:
		# Try to convert to json
		sResult = json.loads(showResult)
		managedDiskName = sResult["name"]
		managedDiskSize = sResult["diskSizeGb"]
		managedDiskTags = sResult["tags"]
		result = '{"name": "%s", "diskSizeGb": "%s", "tags": %s ' % (managedDiskName, managedDiskSize, json.dumps(managedDiskTags))
	except:
		# Add status to result
		result = '{ "status": "error", "message":"An unexpected issue has occurred at Get managed disk information"}'
		return result
	 
	# Delete managed disk
	try:
		# Delete managed disk command"
		deleteCommand = 'az disk delete -n "{0}" -g "{1}" --yes --verbose'.format(managedDiskName, resourceGroup)
		# Execute command"
		delResult = subprocess.check_output(deleteCommand, shell=True)
		# Check result"
		if json.loads(delResult)["status"] == 'Succeeded':
			# Add status to result
			result = result + ', "status": "Succeeded"}'
			return result
		else:
			# Add status to result
			result = result + ', "status": "error"}'
			return result
	except:
		# Add status to result
		result = result + ', "status": "error", "message":"An unexpected issue has occurred at Delete managed disk"}'
		# Give back the result
		return result


# FUNCTION Convert vhd to managed disk
def convertVhdToManagedDisk(sourceVhdUri, targetResourceGroup, targetLocation, managedDiskName, managedDiskSize, managedDiskTags = "'component=ManagedDisk' 'billing=customer'", managedDiskAccountType = "Standard_LRS"):
	# Check parameters
	## Sku for managed disk
	if (managedDiskAccountType == "Standard_LRS") or (managedDiskAccountType == "Premium_LRS"):
		# Source VHD related parameters
		if len(sourceVhdUri) > 10:
			# Check managed disk parameters
			if (len(targetResourceGroup) > 3) and (len(targetLocation) > 5) and (len(managedDiskName) > 3) and (int(managedDiskSize) > 1):
				try:
					# Create command for convert
					convertCommand = "az disk create -n '{0}' -g '{1}' -l '{2}' -z {3} --source '{4}' --sku '{5}' --tags {6} --verbose".format(managedDiskName, targetResourceGroup, targetLocation, managedDiskSize, sourceVhdUri, managedDiskAccountType, managedDiskTags)
					# Execute command
					result = subprocess.check_output(convertCommand, shell=True)
					# Check result
					if json.loads(result)["provisioningState"] == 'Succeeded':
						# Succeeded
						return True
					else:
						# Not succeeded
						return False
				except:
					return False
			else:
				# Wrong parameters
				sys.stdout.write("Managed disk related input parameters do not meet the requirements" + '\n')
				return False
		else:
			# Wrong source parameters
			sys.stdout.write("Source related input parameters do not meet the requirements" + '\n')
			return False
	else:
		# Sku parameters is wrong
		sys.stdout.write("managedDiskAccountType parameter does not meet the requirements" + '\n')
		return False


# FUNCTION convert Tags from json to Azure tags
def tagsToAzure(tags):
	# init result
	result = ""
	# Init json Object
	jsonString = ""
	# try to convert input to json
	try:
		jsonString = json.loads(tags)
	except:
		# resturn with error
		return False

	# Seek on tags
	for currentTag in jsonString:
		# Add tags to reult
		result = result + "'{0}={1}' ".format(currentTag, jsonString["{0}".format(currentTag)])
	
	# Check result
	if len(result) > 4:
		return result
	else:
		# If too short gives back false
		return False

# FUNCTION Copy vhdfrom restore container to original location
def copyUnmanagedDisk(storageAccount, secretKey, sourceVhd, sourceContainer, targetVhd, targetContainer = "vhds", sourceStorageAccount = "", sourceSecretKey = ""):
	# Set init parameters
	ifSourceExists = False
	ifTargedExists = True
	# Set source storage account values if necessary
	if len(sourceStorageAccount) == 0:
		sourceStorageAccount = storageAccount
		sourceSecretKey = secretKey

	### Check target vhd
	# Create show command
	showCommand = "az storage blob show -c '{0}' --account-key '{1}' --account-name '{2}'  -n '{3}'".format(targetContainer, secretKey, storageAccount, targetVhd)
	# Execute show command
	showResult = subprocess.check_output(showCommand, shell=True)
	# Check result
	if len(showResult) == 0:
		# Set variable to True
		ifTargedExists = False
	
	### Check source vhd
	# Create show command
	showCommand = "az storage blob show -c '{0}' --account-key '{1}' --account-name '{2}'  -n '{3}'".format(sourceContainer, sourceSecretKey, sourceStorageAccount, sourceVhd)
	# Execute show command
	showResult = subprocess.check_output(showCommand, shell=True)
	# Check result
	try:
		# Convert to json
		sResult = json.loads(showResult)
		# compare result
		if sResult["name"] == sourceVhd:
			# Set variable to True
			ifSourceExists = True
	except:
		# Error at checking
		return False
	#if exists start Deletion
	if  ifSourceExists and (not ifTargedExists):
		 # Start copy
		try:
			# Create delete command
			copyCommand = "az storage blob copy start --source-account-name '{0}' --source-account-key '{1}' --source-container '{2}' --source-blob '{3}' --account-name '{0}' --account-key '{1}' --destination-container '{4}' --destination-blob '{5}'".format(sourceStorageAccount, sourceSecretKey, sourceContainer, sourceVhd, targetContainer, targetVhd)
			# Execute delete command
			copyResult = subprocess.check_output(copyCommand, shell=True)
			# Check result"
			if  json.loads(copyResult)["status"] == "success":
				# Copied
				return True
		except:
			# Error at deletion
			return False
	else:
		# Source does not exist or target exists
		return False

# FUNCTION Restore Managed disk from vhd
def restoreManagedDiskFromVhd(vmName, resourceGroup, location, sourceStorageAccount, sourceSecretKey, sourceContainer, managedDiskAccountType = "Standard_LRS"):
	# Init message
	messenger("FUNCTION Restore Managed disk from vhd")
	# init results
	osResult = False
	dataResult = 0
	dataIndex = 0
	messenger("Get restore file from restored container")
	# Get restore file from restored container
	fileNameResult = getFileName(sourceStorageAccount, sourceSecretKey, sourceContainer)
	if ".json" in (json.loads(fileNameResult)["type"]):
		messenger("Download deploy file")
		# Download deploy file
		downloadResult = downloadDeployFile(sourceStorageAccount, sourceSecretKey, sourceContainer, json.loads(fileNameResult)["name"], json.loads(fileNameResult)["type"])
		if downloadResult:
			messenger("Check {0} file encoding".format(json.loads(fileNameResult)["type"]))
			# Check file encoding
			if convertFiletoText(json.loads(fileNameResult)["type"]):
				messenger("Deallocate VM: " + vmName)
				# Deallocate VM
				if deallocateVM(vmName, resourceGroup):
					messenger("Delete VM object: " + vmName)
					# Delete VM object
					if deleteVmObject(vmName, resourceGroup):
						messenger("- OS DISK")
						### OS DISK
						messenger("Get os disk information")
						# Get os disk information
						osDiskUri = getOSDiskVhdInfo(json.loads(fileNameResult)["type"])
						# Check result with convert to JSON
						try:
							# Restored disk uri
							sourceVhdUri = json.loads(osDiskUri)["uri"]
							messenger("Delete old managed disk: {0}-osdisk".format(vmName))
							# Delete old managed disk
							deleteResult = deleteManagedDisk("{0}-osdisk".format(vmName), resourceGroup)
							if json.loads(deleteResult)["status"] != "error":
								messenger("Convert old OS Disk tags to right format")
								# Convert os Disk tags to right format
								osDiskTags = tagsToAzure(json.dumps(json.loads(deleteResult)["tags"]))
								# Check tag conversation result
								if osDiskTags != False:
									messenger("Convert vhd to managed disk")
									# Convert vhd to managed disk
									osResult = convertVhdToManagedDisk(sourceVhdUri, resourceGroup, location, json.loads(deleteResult)["name"], json.loads(deleteResult)["diskSizeGb"], osDiskTags, managedDiskAccountType)
							else:
								# Manage disk deletion error
								return False
						except:
							# Restored OS Disk info failed
							return False

						# Manage datadisks if os disk was success
						if osResult:
							messenger("- DATA DISKS")
							### DATA DISKS
							messenger("Get data disks information")
							# Get data disk information
							dataDiskUri = getDataDiskVhdInfo(json.loads(fileNameResult)["type"])
							# Check result...
							try:
								# ...and seek on datadisks
								for disk in json.loads(dataDiskUri)["dataDisks"]:
									# Increase data index
									dataIndex = dataIndex + 1
									# Restored disk uri
									sourceVhdUri = disk["uri"]
									# Create important data
									diskID = disk["lun"] + 1
									messenger("Delete old managed disk: {0}-datadisk-{1}".format(vmName, diskID))
									# Delete old managed disk
									deleteResult = deleteManagedDisk("{0}-datadisk-{1}".format(vmName, diskID), resourceGroup)
									if json.loads(deleteResult)["status"] != "error":
										messenger("Convert old Data Disk tags to right format")
										# Convert os Disk tags to right format
										dataDiskTags = tagsToAzure(json.dumps(json.loads(deleteResult)["tags"]))
										# Check tag conversation result
										if dataDiskTags != False:
											messenger("Convert vhd to managed disk: {0}-datadisk-{1}".format(vmName, diskID))
											# Convert vhd to managed disk
											convertResult = convertVhdToManagedDisk(sourceVhdUri, resourceGroup, location, json.loads(deleteResult)["name"], json.loads(deleteResult)["diskSizeGb"], dataDiskTags, managedDiskAccountType)
											if convertResult:
												# Increase data result value
												dataResult = dataResult + 1
									else:
										# Manage disk deletion error
										return False
								####### Give back final result
								if osResult and (dataResult == dataIndex):
									messenger("OS and Data disks are restored")
									# OS and DataDisks are restored
									return True
								else:
									messenger("OS and/or DataDisks are not restored")
									# OS and/or DataDisks are not restored
									return False
								##############################
									
							except:
								messenger("Restored data info failed")
								# Restored data info failed
								return False
						else:
							messenger("OS disk related activities were not success")
							# os disk related activities were not success
							return False
			else:
				messenger("File conversation error - deleteVmObject")
				# File conversation error deleteVmObject
				return False
		else:
			messenger("File download issue has occurred")
			# File download issue
			return False
	else:
		messenger("Wrong filename")
		# File name issue
		return False

# FUNCTION Restore Unmanaged disk based VM's vhds
def restoreUnmanagedDiskFromVhd(vmName, resourceGroup, location, storageAccount, secretKey, sourceContainer, vmContainer = "vhds", sourceStorageAccount = "", sourceSecretKey = ""):
	# Init message
	messenger("FUNCTION Restore Unmanaged disk based VM's vhds")
	# init results
	osResult = False
	dataResult = 0
	dataIndex = 0
	# Set source storage account values if necessary
	if len(sourceStorageAccount) == 0:
		sourceStorageAccount = storageAccount
		sourceSecretKey = secretKey

	messenger("Get restore file from restored container")
	# Get restore file from restored container
	fileNameResult = getFileName(storageAccount, secretKey, sourceContainer)
	if ".json" in (json.loads(fileNameResult)["type"]):
		messenger("Download deploy file")
		# Download deploy file
		downloadResult = downloadDeployFile(storageAccount, secretKey, sourceContainer, json.loads(fileNameResult)["name"], json.loads(fileNameResult)["type"])
		if downloadResult:
			messenger("Check {0} file encoding".format(json.loads(fileNameResult)["type"]))
			# Check file encoding
			if convertFiletoText(json.loads(fileNameResult)["type"]):
				messenger("Deallocate VM: " + vmName)
				# Deallocate VM
				if deallocateVM(vmName, resourceGroup):
					messenger("Delete VM object: " + vmName)
					# Delete VM object
					if deleteVmObject(vmName, resourceGroup):
						messenger("- OS DISK")
						### OS DISK
						messenger("Get os disk information")
						# Get os disk information
						osDiskUri = getOSDiskVhdInfo(json.loads(fileNameResult)["type"])
						# Check result with convert to JSON
						try:
							# Restored disk uri
							sourceVhdName = json.loads(osDiskUri)["name"]
							messenger("Delete old unmanaged disk: {0}-osdisk.vhd".format(vmName))
							# Delete old unmanaged disk
							deleteResult = deleteUnmanagedDisk("{0}-osdisk.vhd".format(vmName), storageAccount, secretKey, vmContainer)
							if deleteResult:
								messenger("Copy os vhd to its original location")
								# Copy os disk to its original location
								osResult = copyUnmanagedDisk(storageAccount, secretKey, sourceVhdName, sourceContainer, "{0}-osdisk.vhd".format(vmName), "vhds", sourceStorageAccount, sourceSecretKey)
							else:
								messenger("Disk deletion error has occurred")
								# Disk deletion error
								return False
						except:
							messenger("Restored os disk info failure")
							# Restored OS Disk info failed
							return False

						# Manage datadisks if os disk was success
						if osResult:
							messenger("- DATA DISKS")
							### DATA DISKS
							messenger("Get data disks information")
							# Get data disk information
							dataDiskUri = getDataDiskVhdInfo(json.loads(fileNameResult)["type"])
							# Check result...
							try:
								# ...and seek on datadisks
								for disk in json.loads(dataDiskUri)["dataDisks"]:
									# Increase data index
									dataIndex = dataIndex + 1
									# Restored disk uri
									sourceVhdName = disk["name"]
									# Create important data
									diskID = disk["lun"]
									messenger("Delete old data disks vhd files")
									# Delete old unmanaged disk
									deleteResult = deleteUnmanagedDisk("{0}-datadisk-{1}.vhd".format(vmName, diskID), storageAccount, secretKey, vmContainer)
									if deleteResult:
										messenger("Copy data disk to its original location: {0}-datadisk-{1}.vhd".format(vmName, diskID))
										# Copy data disk to its original location
										copyResult = copyUnmanagedDisk(storageAccount, secretKey, sourceVhdName, sourceContainer, "{0}-datadisk-{1}.vhd".format(vmName, diskID), "vhds", sourceStorageAccount, sourceSecretKey)
										# Check result
										if copyResult:
											# Increase data result value
											dataResult = dataResult + 1
									else:
										messenger("Disk deletion error has occurred")
										# Disk deletion error
										return False
								####### Give back final result
								if osResult and (dataResult == dataIndex):
									messenger("OS and Data disks are restored")
									# OS and DataDisks are restored
									return True
								else:
									messenger("OS and/or DataDisks are not restored")
									# OS and/or DataDisks are not restored
									return False
								##############################
									
							except:
								messenger("Restored data info failed")
								# Restored data info failed
								return False
						else:
							messenger("OS disk related activities were not success")
							# os disk related activities were not success
							return False
			else:
				messenger("File conversation error - deleteVmObject")
				# File conversation error deleteVmObject
				return False
		else:
			messenger("File download issue has occurred")
			# File download issue
			return False
	else:
		messenger("Wrong filename")
		# File name issue
		return False

# Module has been loaded
messenger("Restore module has been loaded")