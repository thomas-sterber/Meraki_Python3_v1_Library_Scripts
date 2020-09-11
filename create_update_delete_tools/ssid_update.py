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
	update SSID in a network   (rename, enable/disable)

	Calls in wireless.py of Meraki Python library
		https://developer.cisco.com/meraki/api-v1/#!update-network-wireless-ssid
		
		updateNetworkWirelessSsid(self, networkId: str, number: str, **kwargs):


		https://developer.cisco.com/meraki/api-v1/#!update-network-wireless-ssid
		- networkId (string): (required)
		- number (string): (required)
		- name (string): The name of the SSID
		- enabled (boolean): Whether or not the SSID is enabled
		
		more Options:
		
		- authMode (string): The association control method for the SSID 
			('open', 'psk', 'open-with-radius', '8021x-meraki', '8021x-radius', 'ipsk-with-radius' or 'ipsk-without-radius')
		- enterpriseAdminAccess (string): 
			Whether or not an SSID is accessible by 'enterprise' administrators ('access disabled' or 'access enabled') 
		- encryptionMode (string): 
			The psk encryption mode for the SSID ('wep' or 'wpa'). This param is only valid if the authMode is 'psk'
		- psk (string): 
			The passkey for the SSID. This param is only valid if the authMode is 'psk'
		- wpaEncryptionMode (string): 
			The types of WPA encryption. ('WPA1 only', 'WPA1 and WPA2', 'WPA2 only', 'WPA3 Transition Mode' or 'WPA3 only')
		- and more
		
		see:  
			https://developer.cisco.com/meraki/api-v1/#!update-network-wireless-ssid
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
	print('\nOrganizations:')
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




def select_network(organizationId):
	networks = dashboard_call.organizations.getOrganizationNetworks(organizationId)
	# print(json.dumps(networks, indent=2))
	#
	# select org and return org_id
	menue_source = networks
	i = 0
	menue_list = []
	print('\nNetworks in org:')
	print(line)
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', n['name'])
		i += 1
		menue_list.append(n['id'])
	print(line)
	print('\n\nselect the network')
	select = int(input('>>'))
	#
	network_id = menue_list[select]
	return(network_id)



def select_ssid(networkId):
	network_ssids = dashboard_call.wireless.getNetworkWirelessSsids(networkId)
	# print(json.dumps(network_ssids, indent=2))
	#
	# select ssid and return ssid number
	menue_source = network_ssids
	i = 0
	menue_list = []
	print('\nSSIDs in network :')
	print(line)
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', n['name'])
		i += 1
		menue_list.append(n['number'])
	print(line)
	print('\n\nselect the network')
	select = int(input('>>'))
	#
	ssid_number = menue_list[select]
	return(ssid_number)




def update_ssid(networkId, ssid_number):
	# 
	name = input('SSID name :')
	enabled = input('enable (e) / disable (d): ')
	if enabled == 'e':
		enabled = True
	else:
		enabled = False
	#
	update_ssid_number = dashboard_call.wireless.updateNetworkWirelessSsid(networkId, ssid_number, name=name, enabled=enabled)
	# print(json.dumps(update_ssid_number, indent=2))
	print('\n\nNew Config:')
	print(line)
	for n in update_ssid_number:
		print(n)
	print(line)
	#
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


	# run API call
	# ---------------
	#
	organizationId = get_org_id()
	networkId = select_network(organizationId)
	ssid_number = select_ssid(networkId)

	update_ssid = update_ssid(networkId, ssid_number)
	#
	print('DONE !!')





#
