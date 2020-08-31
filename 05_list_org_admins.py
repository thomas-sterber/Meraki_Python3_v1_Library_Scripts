#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# --------------------------------------------------------
#

__author__      = "Thomas Sterber"
__copyright__   = "Copyright Aug 2020"
__license__     = "GPL"
__email__       = "thomas.sterber@meraki.net"
__status__      = "Beta"




info = '''
		**List the dashboard administrators in this organization**
		
		Call in organizations.py of Meraki Python library
			def getOrganizationAdmins(self, organizationId: str):
 
        https://developer.cisco.com/meraki/api-v1/#!get-organization-admins
        - organizationId (string): (required)
'''


# --------------------------------------------------------
# Import Modules
# --------------------------------------------------------
#
import meraki		# Meraki Dashboard Library
import os, json
from get_accesstoken import get_accesstoken



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
	i = 0
	orgidlist = []
	print('\n\nPlease select one Organization')
	for n in organizations:
		number = str(i).zfill(2)
		print(number , n['name'])
		i += 1
		orgidlist.append(n['id'])
	select = int(input('>>'))
	org_id = orgidlist[select]
	return(org_id)
	
	

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
	#
	admins = dashboard_call.organizations.getOrganizationAdmins(organizationId)
	print(json.dumps(admins, indent=2))

	for n in admins:
		print('-----------------------------------------------------')
		print('Admin name     >', n['name'])
		print('EMail          >', n['email'])
		print('Last active    >', n['lastActive'])
		print('Account Status >', n['accountStatus'])
		print('-----------------------------------------------------')


#

        
        
        
        
        
