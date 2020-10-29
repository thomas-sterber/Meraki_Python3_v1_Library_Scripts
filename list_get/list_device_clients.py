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
	list the clients of a device

	Calls in organization.py, devices.py , networks.py , of Meraki Python library
		https://developer.cisco.com/meraki/api-v1/#!get-device-clients
		https://github.com/meraki/dashboard-api-python/blob/master/meraki/api/devices.py

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


def select_device(networkdevices):
	network_devices = []
	for n in networkdevices:
		device = {}
		device['name']		= n['name']
		device['serial']	= n['serial']
		network_devices.append(device)
	# print(network_devices)

	menue_source = network_devices
	i = 0
	menue_list = []
	print(line)
	adjust = 20
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', n['name'].ljust(adjust,' '), n['serial'])
		i += 1
		menue_list.append(n['serial'])
	print(line)
	print('\n\nselect the device')
	select = int(input('>>'))
	#
	deviceSN = menue_list[select]
	# print(deviceSN)
	return(deviceSN)
	


def get_device_clients(deviceSN):
	device_clients = dashboard_call.devices.getDeviceClients(deviceSN)
	# print(json.dumps(device_clients, indent=2))
	return(device_clients)


def print_device_clients(device_clients):
	for n in device_clients:
		adjust = 20
		print(line)
		print('mdnsName '.rjust(adjust,' '), n['mdnsName'])
		print('mac '.rjust(adjust,' '), n['mac'])
		print('ip '.rjust(adjust,' '), n['ip'])
		print('description '.rjust(adjust,' '), n['description'])
		if ('switchport' in n): print('switchport'.rjust(adjust,' '), n['switchport'])
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
	deviceSN = select_device(networkdevices)
	device_clients = get_device_clients(deviceSN)
	#
	print_device_clients(device_clients)
	#





#
