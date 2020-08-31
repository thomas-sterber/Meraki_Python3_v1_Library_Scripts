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
		*List the organizations that the user has privileges on**
			https://developer.cisco.com/meraki/api-v1/#!get-organizations
			
		API call in the organizations.py of Meraki Python library
			def getOrganizations(self)
'''



# --------------------------------------------------------
# Import Modules
# --------------------------------------------------------
#
import meraki		# Meraki Dashboard Library
import os, json
from get_accesstoken import get_accesstoken   # 



# -----------------------------------------------
#  Functions
# -----------------------------------------------
#

def get_API_KEY():
	API_KEY =  get_accesstoken()
	return(API_KEY)




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
	API_KEY = get_API_KEY()   # read API KEY out of file or create new one
	
	# Instantiate a Meraki dashboard API session
	dashboard_call = meraki.DashboardAPI(
		api_key=API_KEY,
		base_url='https://api-mp.meraki.com/api/v1/',
		log_file_prefix=os.path.basename(__file__)[:-3],
		log_path='./logs/',
		print_console=False
		) 

	# run API call
	organizations = dashboard_call.organizations.getOrganizations()
	print(json.dumps(organizations, indent=2))






#
