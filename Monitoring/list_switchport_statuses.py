#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# --------------------------------------------------------
#

__author__      = "Thomas Sterber"
__copyright__   = "Copyright Aug 2020"
__license__     = "GPL"
__email__       = "thomas.sterber@meraki.net"
__status__      = "demo"




info = '''
	list the switchport statuses

	Calls in organization.py, switch.py of Meraki Python library
		https://developer.cisco.com/meraki/api-v1/#!get-device-switch-ports-statuses
		https://github.com/meraki/dashboard-api-python/blob/master/meraki/api/switch.py
		
		
'''




# --------------------------------------------------------
# Import Modules
# --------------------------------------------------------
#
import meraki		# Meraki Dashboard Library
import os, sys, json
from get_accesstoken import get_accesstoken


# --------------------------------------------------------
# definitions
# --------------------------------------------------------
#
line = 80*'-'


# -----------------------------------------------
#  Functions
# -----------------------------------------------
#

def get_API_KEY():
	API_KEY =  get_accesstoken()
	return(API_KEY)


def get_org_id():
	# get orgs call
	organizations = dashboard_call.organizations.getOrganizations()
	# print(json.dumps(organizations, indent=2))
	#
	# select org and return org_id
	menue_source = organizations
	i = 0
	menue_list = []
	print(line)
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', n['name'])
		i += 1
		menue_list.append(n['id'])
	print(line)
	print('\n\nselect the organization')
	select = int(input('>>'))
	#
	org_id = menue_list[select]
	return(org_id)



def get_networks(organizationId):
	networks = dashboard_call.organizations.getOrganizationNetworks(organizationId)
	# print(json.dumps(networks, indent=2))
	#
	# create dictionary {networkname:networkId, ... }
	networksdic = {}
	for n in networks:
		networkName = n['name']
		networkId = n['id']
		networksdic[networkName] = networkId
	# print(networksdic)
	return(networksdic)



def select_network(networksdic):
	# select the network and return the networkID
	menue_source = networksdic				# {networkname:networkId, ... }
	# print(menue_source)
	i = 0
	menue_list = []
	print(line)
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', n)
		i += 1
		menue_list.append(n)
	print(line)
	print('\n\nselect the network')
	select = int(input('>>'))
	#
	networkId = menue_source[menue_list[select]]
	# print(networkId)
	return(networkId)



def get_devices_of_network(networkId):
	networkdevices = dashboard_call.networks.getNetworkDevices(networkId)
	# print(json.dumps(networkdevices, indent=2))
	return(networkdevices)


def select_switch(networkdevices):
	# create list of MS devices
	ms_devices = []
	for n in networkdevices:
		device = {}
		devicemodel = n['model'][:2]		# MR , MS, MV, ..
		if (devicemodel == 'MS'):
			# print('found a switch')
			device['model'] 	= n['model']
			device['name']		= n['name']
			device['serial']	= n['serial']
			device['mac']		= n['mac']
			ms_devices.append(device)
	# print(ms_devices)
	if (ms_devices == []):
		print('no switch available')
		sys.exit(0)
	# select MS device and return SN
	menue_source = ms_devices
	i = 0
	menue_list = []
	print(line)
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', 'MS name : ', n['name'], '    ', 'MS model : ', n['model'], '    ', 'MS serial : ', n['serial'])
		i += 1
		menue_list.append(n['serial'])
	print(line)
	print('\n\nselect the switch')
	select = int(input('>>'))
	#
	deviceSN = menue_list[select]
	# print(deviceSN)
	return(deviceSN)
	


def get_switchport(deviceSN):
	switchports = dashboard_call.switch.getDeviceSwitchPortsStatuses(deviceSN)
	print(json.dumps(switchports, indent=2))
	return(switchports)


def print_switchports(switchports):
	for n in switchports:
		adjust = 20
		print(line)
		print('Port '.rjust(adjust,' '), n['portId'])
		print('Enabled '.rjust(adjust,' '), n['enabled'])
		print('Status '.rjust(adjust,' '), n['status'])
		print('Errors '.rjust(adjust,' '), n['errors'])
		print('Warnings'.rjust(adjust,' '), n['warnings'])
		print('Speed'.rjust(adjust,' '), n['speed'])
		print('Duplex'.rjust(adjust,' '), n['duplex'])
		print('sent kB'.rjust(adjust,' '), n['usageInKb']['sent'])
		print('received kB'.rjust(adjust,' '), n['usageInKb']['recv'])
		print('Clients'.rjust(adjust,' '), n['clientCount'])
		if ('powerUsageInWh' in n):
			print('Power usage Wh'.rjust(adjust,' '), n['powerUsageInWh'])
	return()


#
# --------------------------------------------------------
# Main
# --------------------------------------------------------
#
if __name__ == "__main__":
	os.system('clear')  # clear screen
	print(info)
	print(100*'-','\n\n')
	input('press enter')
	
	# get API key
	API_KEY = get_API_KEY()
	
	# Instantiate a Meraki dashboard API session
	dashboard_call = meraki.DashboardAPI(
		api_key=API_KEY,
		base_url='https://api-mp.meraki.com/api/v1/',
		log_file_prefix=os.path.basename(__file__)[:-3],
		log_path='./logs/',
		print_console=False
		) 


	# run API call		Get inventory of org
	# ---------------
	#
	organizationId = get_org_id()
	networksdic = get_networks(organizationId)				# dictionary {networkname:networkId, ... }
	networkId = select_network(networksdic)
	networkdevices = get_devices_of_network(networkId)
	deviceSN = select_switch(networkdevices)
	switchports = get_switchport(deviceSN)
	#
	print_switchports(switchports)
	#





#
