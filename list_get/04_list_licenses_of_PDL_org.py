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
		**List the licenses for an PDL organization**

		Call in organizations.py of Meraki Python library
			def getOrganizationLicenses(self, organizationId: str, total_pages=1, direction='next', **kwargs):
'''
'''
        https://developer.cisco.com/meraki/api-v1/#!get-organization-licenses
        - organizationId (string): (required)
        - total_pages (integer or string): use with perPage to get total results up to total_pages*perPage; -1 or "all" for all pages
        - direction (string): direction to paginate, either "next" (default) or "prev" page
        - perPage (integer): The number of entries per page returned. Acceptable range is 3 - 1000. Default is 1000.
        - startingAfter (string): A token used by the server to indicate the start of the page. Often this is a timestamp or an ID but it is not limited to those. This parameter should not be defined by client applications. The link for the first, last, prev, or next page in the HTTP Link header should define it.
        - endingBefore (string): A token used by the server to indicate the end of the page. Often this is a timestamp or an ID but it is not limited to those. This parameter should not be defined by client applications. The link for the first, last, prev, or next page in the HTTP Link header should define it.
        - deviceSerial (string): Filter the licenses to those assigned to a particular device
        - networkId (string): Filter the licenses to those assigned in a particular network
        - state (string): Filter the licenses to those in a particular state. Can be one of 'active', 'expired', 'expiring', 'unused', 'unusedActive' or 'recentlyQueued'
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
	try:
		lics = dashboard_call.organizations.getOrganizationLicenses(organizationId)
		print(json.dumps(lics, indent=2))
		for n in lics:
			print('-----------------------------------------------------')
			print('Lic Type        >', n['licenseType'])
			print('Lic Key         >', n['licenseKey'])
			print('Order #         >', n['orderNumber'])
			print('Lic Expire Date >', n['expirationDate'])
			print('-----------------------------------------------------')

	except:
		print('This Org is not an PDL Org')




#

        
        
        
