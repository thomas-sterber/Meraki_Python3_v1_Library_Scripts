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
	update a network  

	Calls in networks.py of Meraki Python library
		https://developer.cisco.com/meraki/api-v1/#!update-network
	
		updateNetwork(self, networkId: str, **kwargs):

		- networkId (string): (required)
		- name (string): The name of the network
		- timeZone (string): The timezone of the network. For a list of allowed timezones, please see the 'TZ' column in the table in <a target='_blank' href='https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'>this article.</a>
		- tags (array): A list of tags to be applied to the network
		- enrollmentString (string): A unique identifier which can be used for device enrollment or easy access through the Meraki SM Registration page or the Self Service Portal. Please note that changing this field may cause existing bookmarks to break.

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



def select_network(organizationId):
	networks = dashboard_call.organizations.getOrganizationNetworks(organizationId)
	# print(json.dumps(networks, indent=2))
	#
	# select org and return org_id
	menue_source = networks
	i = 0
	menue_list = []
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



def update_network(networkId):
	new_name = input('network name : ')
	new_timezone = input('time zone  (America/Los_Angeles, Europe/Berlin,..) :')
	new_tags = []
	newtags = input('tags : (tag1 tag2 .. ) :')
	new_tags.append(newtags)
	#
	network_update = dashboard_call.networks.updateNetwork(
															networkId, 
															name = new_name,
															tags = new_tags, 
															timeZone=new_timezone
															)
	# print(json.dumps(network_update, indent=2))
	



def list_networks(organizationId):
	networks = dashboard_call.organizations.getOrganizationNetworks(organizationId, total_pages=1, direction='next')
	# print(json.dumps(networks, indent=2))
	#
	print(line)
	print("    available networks and networkid's: ")
	print(line)
	adjust = 20
	for n in networks:
		print(n['name'].rjust(adjust,' '), '  ', n['id'])
	return()


#
# --------------------------------------------------------
# Main
# --------------------------------------------------------
#
if __name__ == "__main__":
	os.system('clear')  # clear screen
	print(info)
	print(120*'-','\n\n')
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
	update_network = update_network(networkId)
	
	list_networks(organizationId)
	#
	print('DONE !')





#
