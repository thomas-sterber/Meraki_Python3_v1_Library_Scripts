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
	list L3 firewall rules of mx

	Calls in appliance.py , of Meraki Python library
		
		https://developer.cisco.com/meraki/api-v1/#!get-network-appliance-firewall-l-3-firewall-rules
		
		def getNetworkApplianceFirewallL3FirewallRules(self, networkId: str):
		

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



def get_l3firewallRules(networkId):
	l3fwrules = dashboard_call.appliance.getNetworkApplianceFirewallL3FirewallRules(networkId)
	print(json.dumps(l3fwrules, indent=2))
	return(l3fwrules)


def print_firewall_rules(l3fwrules):
	print('\n\n')
	print('L3 Firewall Rules :')
	print(line)
	l3fwrules = l3fwrules['rules']
	for n in l3fwrules:
		print('Rule :'.rjust(15, ' '), n['comment'])
		print('policy :'.rjust(30, ' '), n['policy'])
		print('protocol :'.rjust(30, ' '), n['protocol'])
		print('src port :'.rjust(30, ' '), n['srcPort'])
		print('dst port :'.rjust(30, ' '), n['destPort'])
		print('dest Cidr :'.rjust(30, ' '), n['destCidr'])
		print('syslogEnabled :'.rjust(30, ' '), n['syslogEnabled'])
		print('\n', line)
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
	l3fwrules = get_l3firewallRules(networkId)
	#
	print_firewall_rules(l3fwrules)




#
