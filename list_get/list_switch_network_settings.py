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
	list the switch network settings of a selected network
		https://developer.cisco.com/meraki/api-v1/#!get-network-switch-settings
		
		call in switch.py
			getNetworkSwitchSettings(self, networkId: str):
			...

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


def get_switch_network_settings(networkId):
	#
	# mgmt_vlan_and_power call
	vlan_and_power = dashboard_call.switch.getNetworkSwitchSettings(networkId)
	# print('mgmt and power\n',json.dumps(vlan_and_power, indent=2))
	#
	# mtu call
	mtu = dashboard_call.switch.getNetworkSwitchMtu(networkId)
	# print('mtu\n',json.dumps(mtu, indent=2))
	#
	# stp call
	stp = dashboard_call.switch.getNetworkSwitchStp(networkId)
	# print('stp\n',json.dumps(stp, indent=2))
	#
	# acls call
	acls = dashboard_call.switch.getNetworkSwitchAccessControlLists(networkId)
	# print('acls\n',json.dumps(acls, indent=2))
	#
	# qos call
	qos = dashboard_call.switch.getNetworkSwitchQosRules(networkId)
	# print('qos\n',json.dumps(qos, indent=2))
	#
	#mcast call
	mcast =   dashboard_call.switch.getNetworkSwitchRoutingMulticast(networkId)
	# print('mcast\n',json.dumps(mcast, indent=2))
	#
	#
	#
	return(vlan_and_power, mtu, stp, acls, qos, mcast)



def print_switch_network_settings(vlan_and_power, mtu, stp, acls, qos, mcast):
	print(line)
	adjust = 20
	#
	#vlan_and_power
	print('Mgmt vlan and power settings')
	print(line)
	keys = vlan_and_power.keys()
	for key in keys:
		value = vlan_and_power[key]
		print(key.rjust(adjust,' '), '    ', value)
	print(3*'\n')
	#
	# mtu settings
	print('MTU settings')
	print(line)
	keys = mtu.keys()
	for key in keys:
		value = mtu[key]
		print(key.rjust(adjust,' '), '    ', value)
	print(3*'\n')
	#
	# stp settings
	print('STP settings')
	print(line)
	keys = stp.keys()
	for key in keys:
		value = stp[key]
		print(key.rjust(adjust,' '), '    ', value)
	print(3*'\n')
	#
	# acls settings
	print('ACLs config')
	print(line)
	rules = acls['rules']
	for rule in rules:
		print('Rulename :'.rjust(15,' '), rule['comment'])
		print('policy :'.rjust(20,' '), rule['policy'])
		print('ipVersion :'.rjust(20,' '), rule['ipVersion'])
		print('protocol :'.rjust(20,' '), rule['protocol'])
		print('srcCidr :'.rjust(20,' '), rule['srcCidr'])
		print('srcPort :'.rjust(20,' '), rule['srcPort'])
		print('dstCidr :'.rjust(20,' '), rule['dstCidr'])
		print('dstPort :'.rjust(20,' '), rule['dstPort'])
		print('vlan :'.rjust(20,' '), rule['vlan'])
		print(2*'\n')
	print(3*'\n')
	#
	# qos settings
	print('QOS settings')
	print(line)
	i = 1
	for n in qos:
		print('qos rule ',i)
		keys = n.keys()
		for key in keys:
			value = n[key]
			print(key.rjust(adjust,' '), '    ', value)
		i+=1
		print('\n')
	print(3*'\n')
	#
	# mcast settings
	print('MCast settings')
	print(line)
	keys = mcast.keys()
	for key in keys:
		value = mcast[key]
		print(key.rjust(adjust,' '), '    ', value)
	print(3*'\n')
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
	networksdic = get_networks(organizationId)				# dictionary {networkname:networkId, ... }
	networkId = select_network(networksdic)
	vlan_and_power, mtu, stp, acls, qos, mcast = get_switch_network_settings(networkId)
	
	print_switch_network_settings(vlan_and_power, mtu, stp, acls, qos, mcast)





#
