#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# --------------------------------------------------------
#

import time, os, sys
from pathlib import Path

def get_accesstoken():
    print ('\n\n')
    try:
        # read accesstoken out file
        homepath = str(Path.home())
        f = open(homepath + "/accesstoken.dat","r")
        lines = f.readlines()
        f.close()
        accesstoken = lines[0].rstrip()
    except IOError:
        accesstoken = input('What is your API accesstoken ? \n Demo Read-only API key: "15da0c6ffff295f16267f88f98694cf29a86ed87" ')
        q = input('should the accesstoken saved in your home dir ? (y/n)   :' )
        if (q == 'y'):
            homepath = str(Path.home())
            f = open(homepath + "/accesstoken.dat","w")
            f.write(accesstoken)
            f.close()
    return(accesstoken)


#
# --------------------------------------------------------
# Main
# --------------------------------------------------------
#
if __name__ == "__main__":
    os.system('clear')  # clear screen
    # init
    workdir = os.path.abspath(os.curdir)
    x_cisco_meraki_api_key =  get_accesstoken()
    print(x_cisco_meraki_api_key)
    #

