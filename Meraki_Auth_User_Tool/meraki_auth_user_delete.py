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
	Delete Meraki Auth User
	
	802.1X       == Wifi 802.1X user
	Guest        == Wifi Splashaccess user
	Client VPN   == MX Client VPN user
	

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



def get_network_users(networkId):
	network_users = dashboard_call.networks.getNetworkMerakiAuthUsers(networkId)
	# print(json.dumps(network_users, indent=2))
	return(network_users)


def create_users_dic(network_users):
	# create dictionary {userName:userId}
	users_dic = {}
	for n in network_users:
		if (n["accountType"] != 'Administrator'):
			userName_accountType = n['name'] + '_' + n['accountType']
			userId   = n['id']
			users_dic[userName_accountType] = userId
	# print(users_dic)
	return(users_dic)
 


def select_network_user(users_dic):
	# select the user and return the merakiAuthUserId
	menue_source = users_dic				# {userName:userId}
	# print(menue_source)
	i = 0
	menue_list = []
	print('\nAvailable Users:')
	print(line)
	for n in menue_source:
		number = str(i).rjust(4, ' ')
		print(number, '    ', n)
		i += 1
		menue_list.append(n)
	print(line)
	print('\n\nselect the user to delete')
	select = int(input('>>'))
	#
	merakiAuthUserId = menue_source[menue_list[select]]
	# print(merakiAuthUserId)
	return(merakiAuthUserId)



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


def delete_network_user(networkId ,merakiAuthUserId):
	delUser = dashboard_call.networks.deleteNetworkMerakiAuthUser(networkId ,merakiAuthUserId)
	# print(json.dumps(delUser, indent=2))
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
	network_users = get_network_users(networkId)
	users_dic = create_users_dic(network_users)
	merakiAuthUserId = select_network_user(users_dic)
	#
	del_user = delete_network_user(networkId ,merakiAuthUserId)
	#
	network_users = get_network_users(networkId)
	show_network_users(network_users)
	#
	


#
