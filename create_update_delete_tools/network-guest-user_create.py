#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# --------------------------------------------------------
#

__author__      = "Thomas Sterber"
__copyright__   = "Copyright Oct 2020"
__license__     = "GPL"
__email__       = "thomas.sterber@meraki.net"
__status__      = "demo"




info = '''
	Create guest user    , Splash access user   (AccountType == Guest)
	
			currently, organizations have a 50,000 user cap)
	
	https://developer.cisco.com/meraki/api-v1/#!create-network-meraki-auth-user
	
	
	
	!! at least one Splash wifi ssid needs to be available
	   auth type == open
	   splash:  sign on with meraki splash authentication

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
	print('\nAvailable Orgs:')
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
	print('\nAvailable Networks:')
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


def get_ssidNumbers(networkId):   
	# create dictionary  ' ssidName:ssidNumber ' for all SSIDs with authMode 802.1X Meraki and "splashPage": "None"
	network_ssids = dashboard_call.wireless.getNetworkWirelessSsids(networkId)
	print(json.dumps(network_ssids, indent=2))
	#
	ssids_dic = {}
	for n in network_ssids:
		# check for "authMode": "open" and "splashPage": "Password-protected with Meraki RADIUS"
		if ((n["authMode"] == "open") and (n["splashPage"] == "Password-protected with Meraki RADIUS")):
			ssids_dic[n['name']]=n['number']
	if (ssids_dic == {}):
		print('no Wifi SSID available for Splash with Meraki Auth')
		sys.exit(0)
	print(ssids_dic)
	return(ssids_dic)



def select_ssid(ssids_dic):
	# select SSID and return SSID number
	menue_source = ssids_dic				# {ssidname: ssidnumber, ...}
	i = 0
	menue_list = []
	print('\nAvailable SSIDs:')
	print(line)
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', n)
		i += 1
		menue_list.append(n)
	print(line)
	print('For which SSID the user should get access ?')
	print('\n\nselect the SSID ')
	select = int(input('>>'))
	#
	ssidNumber= menue_source[menue_list[select]]
	# print(ssidNumber)
	return(ssidNumber)



def get_network_users(networkId):
	network_users = dashboard_call.networks.getNetworkMerakiAuthUsers(networkId)
	# print(json.dumps(network_users, indent=2))
	return(network_users)



def show_network_users(network_users):
	print(line)
	print("    available users: ")
	print(line)
	adjust = 20
	for n in network_users:
		if (n['accountType'] != "Administrator"):		# don't print Administrators
			print(n['name'])
			print('\tAccountType  ', '    ' , n['accountType'])
			print('\tAuthZone     ', '    ' , n['authorizations'][0]['authorizedZone'])
			print('\tExpires      ', '    ' , n['authorizations'][0]['expiresAt'])
			print('\n')
	return()



def create_guest_user(networkId, ssidNumber):     # Wifi 802.1X user
	name 			= input('User Name : ')
	email 			= input('User EMail : ')
	password 		= input('User Passwd : ')
	authorizations 	= [{"expiresAt": "Never", "ssidNumber": ssidNumber}]
	accountType 	= 'Guest'
	emailPasswordToUser = False
	#
	newUser = dashboard_call.networks.createNetworkMerakiAuthUser(
									networkId, 
									email, 
									name, 
									password, 
									authorizations=authorizations, 
									accountType=accountType, 
									emailPasswordToUser=emailPasswordToUser
									)
	# print(json.dumps(newUser, indent=2))
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
	networksdic = get_networks(organizationId)
	networkId = select_network(networksdic)
	#
	ssids_dic = get_ssidNumbers(networkId)  # only SSIDs with auth Mode 802.1X-Meraki
	ssidNumber = select_ssid(ssids_dic)
	#
	new_user = create_guest_user(networkId, ssidNumber)
	#
	network_users = get_network_users(networkId)
	show_network_users(network_users)
	#
	








#
