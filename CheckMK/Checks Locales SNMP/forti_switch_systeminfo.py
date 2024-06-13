#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#move the plugin to the folder /opt/omd/sites/nameofsite/local/lib/check_mk/base/plugins/agent_bhistoryased
#chown in the script for the user site (name of site)
#execute in OMD "cmk --debug -I --detect-plguins=nameofplugin -v"

#                                         o8o      .               
#                                         `"'    .o8             
# ooo. .oo.    .ooooo.  oooo oooo    ooo oooo  .o888oo  .oooo.    
# `888P"Y88b  d88' `88b  `88. `88.  .8'  `888    888   `P  )88b    
#  888   888  888ooo888   `88..]88..8'    888    888    .oP"888    
#  888   888  888    .o    `888'`888'     888    888 . d8(  888   
# o888o o888o `Y8bod8P'     `8'  `8'     o888o   "888" `Y888""8o 

from .agent_based_api.v1 import *
import pprint
import re

def discover_sysinfo(section):
    name = "System Info"
    yield Service(item=name)

def check_sysinfo(item, section):
    for i in section:
        if item == "System Info":
            if not i:
                yield Result(state = State.CRIT, summary = f"No system info")
            else:
                i = ' '.join(i)
                yield Result(state = State.OK, summary = f"{i}")
        return

register.check_plugin(
    name="fortiswitch_systeminfo",
    service_name="%s",
    discovery_function = discover_sysinfo,
    check_function=check_sysinfo,
)

register.snmp_section(
    name = "fortiswitch_systeminfo",
    detect = exists(".1.3.6.1.4.1.12356.106.4.1.1"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12356.106.4.1.1",
        oids=[
            "0", 
],
    ),
)

