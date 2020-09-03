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
		**List the clients that have used this network in the timespan of 30 days**

		call is in networks.py
		getNetworkClients(self, networkId: str, total_pages=1, direction='next', **kwargs):
        """
        
        https://developer.cisco.com/meraki/api-v1/#!get-network-clients
'''
'''
		30 days = 30*24*60*60 = 2592000 secs
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




def get_network_clients(networkId):
	timespan=2592000			# 30 days in seconds
	perPage=500					# 
	total_pages=-1				# -1 == all
	#
	clients = dashboard_call.networks.getNetworkClients(networkId, timespan=timespan, perPage=perPage, total_pages=total_pages)
	# print(json.dumps(clients, indent=2))
	return(clients)



def print_clients(clients):
	for n in clients:
		print(line)
		print('Name'.rjust(20,' '), n['description'])
		print('Status'.rjust(20,' '), n['status'])
		print('MAC'.rjust(20,' '), n['mac'])
		print('IP'.rjust(20,' '), n['ip'])
		print('OS'.rjust(20,' '), n['os'])
		print('VLAN'.rjust(20,' '), n['vlan'])
		print('GroupPolicy'.rjust(20,' '), n['groupPolicy8021x'])
		print('LastSeen'.rjust(20,' '), n['lastSeen'])
		print(2*'\n')


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
	#
	organizationId = get_org_id()
	networksdic = get_networks(organizationId)				# dictionary {networkname:networkId, ... }
	networkId = select_network(networksdic)
	clients = get_network_clients(networkId)
	#
	print_clients(clients)





#
