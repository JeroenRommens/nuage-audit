# Nuage-Audit: Get an overview of your Nuage deployment

**NOTE: This package is considered Alpha quality.

## Overview

This is a Python script which can be used to retrieve an overview of what objects are configured in the VSD. The script uses the Python VSPK to fetch all data from the VSD.

## Prerequisites

This script can be run from any host as long as the following prerequesites are met:

1. Python VSPK package is installed
1. There is IP connectivity between the host that will run the script and the VSD

## Running the script

	python nuage_audit.py --vsd 10.167.1.60 --enterprise 'Enterprise X'

## Example Output
	Jeroens-MacBook-Pro:nuage-audit jrommens$ python nuage_audit.py --vsd 10.167.1.60 --enterprise 'vns0'
	--------------------------
	Printing VSD Audit Summary
	--------------------------
	Enterprise Name: vns0
	Number of L3 domains: 2
	L3 Domain details: 
		L3 DOm :
			 Zones: 3
			 Subnets: 4
			 Number of vPorts: 3 (Type Bridge: 3 Type Host: 0)
			 Underlay Breakout settings: Underlay Enabled: ENABLED PAT Enabled: ENABLED
			 DPI Setting: DISABLED
			 Ingress ACL Rules:
				 Name: Allow All Active: True Default Allow IP: True Default Allow Non IP: True Allow Address Spoofing: True
					 Priority: 100 Description: Allow BGP Source: ANY Destination: ANY Protocol: 6
					 Source Port: * Destination Port: 179 Action: FORWARD
					 Stateful: True Stats Logging Enabled: True Flow Logging Enabled: True
	
					 Priority: 200 Description: Drop HTTP Source: ANY Destination: ANY Protocol: 6
					 Source Port: * Destination Port: 80 Action: DROP
					 Stateful: False Stats Logging Enabled: True Flow Logging Enabled: False
	
			 Egress ACL Rules:
				 Name: Allow All Active: True Default Allow IP: True Default Allow Non IP: True Install ACL Implicit Rules: True
		L3 Test :
			 Zones: 0
			 Subnets: 0
			 Number of vPorts: 0 (Type Bridge: 0 Type Host: 0)
			 Underlay Breakout settings: Underlay Enabled: DISABLED PAT Enabled: DISABLED
			 DPI Setting: DISABLED
			 Ingress ACL Rules:
				  None Defined 
			 Egress ACL Rules:
				  None Defined 
	Infrastructure Details: 
		Number of Network Services Gateways configured: 8 (Status Active: 5 Other: 3)
		Personality distribution: NSG: 6 NSG-BR: 1 NSG-UBR: 1
		Single/Dual Uplink distribution (only including personality NSG): Single Uplink: 5 Dual Uplink: 1
		Uplink connection distribution (only including personality NSG): Dynamic: 4 Static: 1 PPPoE: 1 LTE: 0
		Number of uplinks with NAT probes enabled: 13
		Number of uplinks with Traffic Through UBR Only flag enabled: 1
		Number of uplinks with an IKE tunnel configured: 1
		Number of uplinks with BGP configured: 1
		Number of uplinks with a PAT Pool configured: 1
		Number of uplinks with Egress QoS Profile: 1
	--------------------------

