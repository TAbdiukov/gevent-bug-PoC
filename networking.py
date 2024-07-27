#!/usr/bin/env python
# -*- coding: utf8 -*-

import ipaddress
import urllib.parse

import logging
logging.basicConfig(level=logging.DEBUG)

def httpUrlDecode_RFC(data:str) -> str:
	"""
	This function decodes a URL-encoded string. RFC 3986-compliant.
	Args:
		data (str): A URL-encoded string.

	Returns:
		str: The decoded string. URL-encoded characters (which start with a '%' followed by two hexadecimal digits) are decoded and replaced in the string.

	"""
	return urllib.parse.unquote_to_bytes(data).decode("UTF-8")

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
	# safe_host now can be like:
	# localhost
	# 127.0.0.1
	# 127.0.0.1:6000
	# [2001:0000:130F:0000:0000:09C0:876A:130B]:4444
	return not(
		'127.0.0.1' in safe_host or
		'0.0.0.0' in safe_host or
		'localhost' in safe_host or
		is_ip_loopback(safe_host)
	)
