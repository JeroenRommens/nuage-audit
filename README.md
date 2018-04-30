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
	Enterprise Name: __vns0__
	Number of L3 domains: __2__
	L3 Domain details: 
		L3 DOm :
			 Zones: __3__
			 Subnets: __4__
			 Number of vPorts: __3__ (Type Bridge: __3__ Type Host: __0__)
			 Underlay Breakout settings: Underlay Enabled: __ENABLED__ PAT Enabled: __ENABLED__
			 DPI Setting: __DISABLED__
			 Ingress ACL Rules:
				 Name: __Allow All__ Active: __True__ Default Allow IP: __True__ Default Allow Non IP: __True__ Allow Address Spoofing: __True__
					 Priority: __100__ Description: __Allow BGP__ Source: __ANY__ Destination: __ANY__ Protocol: __6__
					 Source Port: __*__ Destination Port: __179__ Action: __FORWARD__
					 Stateful: __True__ Stats Logging Enabled: __True__ Flow Logging Enabled: __True__
	
					 Priority: __200__ Description: __Drop HTTP__ Source: __ANY__ Destination: __ANY__ Protocol: __6__
					 Source Port: __*__ Destination Port: __80__ Action: __DROP__
					 Stateful: __False__ Stats Logging Enabled: __True__ Flow Logging Enabled: __False__
	
			 Egress ACL Rules:
				 Name: __Allow All__ Active: __True__ Default Allow IP: __True__ Default Allow Non IP: __True__ Install ACL Implicit Rules: __True__
		L3 Test :
			 Zones: __0__
			 Subnets: __0__
			 Number of vPorts: __0__ (Type Bridge: __0__ Type Host: __0__)
			 Underlay Breakout settings: Underlay Enabled: __DISABLED__ PAT Enabled: __DISABLED__
			 DPI Setting: __DISABLED__
			 Ingress ACL Rules:
				  __None Defined__ 
			 Egress ACL Rules:
				  __None Defined__ 
	Infrastructure Details: 
		Number of Network Services Gateways configured: __8__ (Status Active: __5__Other: __3__)
		Personality distribution: NSG: __6__ NSG-BR: __1__ NSG-UBR: __1__
		Single/Dual Uplink distribution (only including personality NSG): Single Uplink: __5__ Dual Uplink: __1__
		Uplink connection distribution (only including personality NSG): Dynamic: __4__ Static: __1__ PPPoE: __1__ LTE: __0__
		Number of uplinks with NAT probes enabled: __13__
		Number of uplinks with Traffic Through UBR Only flag enabled: __1__
		Number of uplinks with an IKE tunnel configured: __1__
		Number of uplinks with BGP configured: __1__
		Number of uplinks with a PAT Pool configured: __1__
		Number of uplinks with Egress QoS Profile: __1__
	--------------------------

