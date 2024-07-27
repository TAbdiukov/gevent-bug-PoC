#!/usr/bin/env python
# -*- coding: utf8 -*-

import ipaddress

import logging
logging.basicConfig(level=logging.DEBUG)

def is_ip_loopback(host:str ) -> bool:
	"""
	Checks if a given host is a loopback IP address.

	Args:
		host (str): The host to check. This can be a string representation of an IPv4 or IPv6 address.

	Returns:
		bool: True if the host is a loopback IP address, False otherwise. If the host is not a valid IP address, the function also returns False.
	"""
	try:
		ip = ipaddress.ip_address(host)
		return ip.is_loopback
	except ValueError:
		return False

def is_host_egress(host:str) -> bool:
	"""
	Checks if the given host is egress.

	Args:
		host (str): The host to be checked.

	Returns:
		bool: True if the host is not None, not equal to Cfg.HOST, not 'localhost', not '0.0.0.0' and not an IP loopback. False otherwise.
	"""
	# Extract the host part of the URL
	if(host is None):
		return False

	safe_host = host.split("://")[-1]
	safe_host = safe_host.split("/")[0]
	return not(
		'127.0.0.1' in safe_host or
		'0.0.0.0' in safe_host or
		'localhost' in safe_host or
		is_ip_loopback(safe_host)
	)
