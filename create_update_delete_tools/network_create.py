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
	create a new network for an organization

	Calls in organization.py of Meraki Python library
		https://developer.cisco.com/meraki/api-v1/#!create-organization-network
	
		createOrganizationNetwork(self, organizationId: str, name: str, productTypes: list, **kwargs):

		- organizationId (string): (required)
		- name (string): The name of the new network
		- productTypes (array): The product type(s) of the new network. Valid types are wireless, appliance, 
				switch, systemsManager, camera, cellularGateway. If more than one type is included, 
				the network will be a combined network.
		- tags (array): A list of tags to be applied to the network
		- timeZone (string): The timezone of the network. For a list of allowed timezones, please see
				https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
		- copyFromNetworkId (string): The ID of the network to copy configuration from. 
				Other provided parameters will override the copied configuration, except type which must 
				match this network's type exactly.


	!! for network of type combined   (wireless, appliance, switch, systemsManager, camera and cellularGateway)
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



def create_network(organizationId):
	networkname = input('Networkname : ')
	# 
	name = networkname
	productTypes = [
							"appliance",
							"switch",
							"camera",
							"wireless",
							"cellularGateway",
							"systemsManager"
							]
	timeZone = "Europe/Berlin"				# see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
	tags = [ "new_network test_network" ]	# 2 tags 
	#
	
	
	
	#
	new_network = dashboard_call.organizations.createOrganizationNetwork(
																		organizationId, 
																		name, 
																		productTypes, 
																		tags = tags, 
																		timeZone=timeZone
																		)
	# print(json.dumps(new_network, indent=2))
	return()



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
	create_network(organizationId)
	
	list_networks(organizationId)
	#
	Print('DONE !')





#
