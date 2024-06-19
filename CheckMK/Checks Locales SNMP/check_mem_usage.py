#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#move the plugin to the folder /opt/omd/sites/nameofsite/local/lib/check_mk/base/plugins/agent_based
#chown in the script for the user site (name of site)
#execute in OMD "cmk --debug -I --detect-plguins=nameofplugin -v"
from .agent_based_api.v1 import *
import pprint
import re

def discover_fortiadc_memory(section):
    yield Service(item="Memory used")

def check_fortiadc_memory(item, section):
    for i in section:
        if item == "Memory used":
            yield Metric("mem_used", int(i[0]))
            if int(i[0]) >= 90:
                yield Result(state = State.CRIT, summary = f"Memory used - {i[0]}%")
                return
            elif int(i[0]) >= 85:
                yield Result(state = State.WARN, summary = f"Memory used - {i[0]}%")
                return
            else:
                yield Result(state = State.OK, summary = f"Memory used - {i[0]}%")
                return

register.check_plugin(
    name="fortiswitch_memory",
    service_name="%s",
    discovery_function = discover_fortiadc_memory,
    check_function=check_fortiadc_memory,
)

register.snmp_section(
    name = "fortiswitch_memory",
    detect = exists(".1.3.6.1.4.1.12356.106.4.1.2"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.12356.106.4.1.2",
        oids=[
            "0",],
    ),
)
