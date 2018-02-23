#!/usr/bin/python

""" Module: amaretto core
	Function collection for Core azure functions
	
	Version: 1.1.0.0
	Last modified date: 22.02.2018.

	Usage:
	from amarettocore import *
"""

import io
import json
import sys
import subprocess


# Check Python version
PVER = 0
if sys.version_info[0] == 2:
	PVER = 2
elif sys.version_info[0] == 3:
	PVER = 3
else:
	sys.exit("Python version does not meet the requirements. Version number: {0}".format(sys.version_info[0]))

# FUNCTION Login to Azure
def azureLogin():
	# Get Azure environment related parameters
	subscriptionLocation = ""
	subscriptionCloud = ""
	subscriptionId = ""

	# Get subscriptionCloud for login
	message = "Please type the subscriptionCloud for Azure subscription (eg. 'AzureGermanCloud'): "
	if PVER == 2:
		subscriptionCloud = raw_input(message)
	else:
		subscriptionCloud = input(message)

	# Get subscriptionLocation for login
	message = "Please type the subscriptionLocation for Azure subscription (eg. 'germanycentral'): "
	if PVER == 2:
		subscriptionLocation = raw_input(message)
	else:
		subscriptionLocation = input(message)

	# Get subscriptionId for login
	message = "Please type the subscriptionId for Azure subscription: "
	if PVER == 2:
		subscriptionId = raw_input(message)
	else:
		subscriptionId = input(message)

	# Set Azure environment name
	resultCode = 0
	try:
		bashcmd = "az cloud set --name {0}".format(subscriptionCloud)
		result = subprocess.check_output(bashcmd, shell=True)

	# Error handling
	except subprocess.CalledProcessError as grepexc:
		resultCode = grepexc.returncode
		sys.exit("Cloud setting error")


	# Check result
	if resultCode == 0:
		# Everything is OK
		resultCode = 0
		jResult = ""
		# Check should I have to login or not
		
		# Get username for login
		if PVER == 2 :
			userName = raw_input("Please type the username for '{0}' subsription: ".format(subscriptionId))
		else:
			userName = input("Please type the username for '{0}' subsription: ".format(subscriptionId))
		try:
			# Login to Azure
			bashcmd = "az login -u {0}".format(userName)
			result = subprocess.check_output(bashcmd, shell=True)
			jResult = json.loads(result)
			
		# Error handling
		except subprocess.CalledProcessError as grepexc:
			resultCode = grepexc.returncode
			sys.exit("Login Error")

# FUNCTION Set default subscription
def defaultSubscription(subscriptionID):
	# Create command
	bashcmd = "az account set --subscription {0}".format(subscriptionID)
	# Execute command
	try:
		result = subprocess.check_output(bashcmd, shell=True)
		return True
	except:
		return False

# FUNCTION Get default subscription
def getDefaultSubscription():
	# init result
	result = '{"error": "No default subscription. You have to login to Azure."}'
	# Create command
	bashcmd = "az account show"
	# Execute command
	try:
		result = subprocess.check_output(bashcmd, shell=True)
		# Convert to json
		jResult = json.loads(result)
		# Create result
		result = '{ "environmentName": "%s", "subscriptionId": "%s", "subscriptionName": "%s", "userName": "%s" }' % (jResult["environmentName"], jResult["id"], jResult["name"], jResult["user"]["name"],)
		return result
	except:
		return result