#!/usr/bin/env python
# -*- coding: utf8 -*-

import ipaddress
import urllib.parse

import logging
logger = logging.getLogger(__name__)

def httpUrlDecode_RFC(data:str) -> str:
	"""
	This function decodes a URL-encoded string. RFC 3986-compliant.
	Args:
		data (str): A URL-encoded string.

	Returns:
		str: The decoded string. URL-encoded characters (which start with a '%' followed by two hexadecimal digits) are decoded and replaced in the string.

	"""
	return urllib.parse.unquote_to_bytes(data).decode("UTF-8")

def is_ip_loopback(host:str) -> bool:
	"""
	NETWORKING function
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

def is_port_valid(port) -> bool:
	try:
		port = int(port)
		assert(port >= 0)
		assert(port <= 0xFFFF)
	except (AssertionError, AttributeError, ValueError, IndexError):
		return False
	return True

def separate_last_delimited_value(s:str, delim:str=":"):
	if(not s):
		return s, ""

	parts = s.split(delim)

	if len(parts) <= 1:
		return s, ""

	last = parts[-1] if parts[-1] != delim else ""

	return delim.join(parts[:-1]), last

def try_extract_bare_host_and_port(any_host:str):
	try:
		assert(any_host)
		host, port = separate_last_delimited_value(any_host)

		assert(host)
		assert(port)

		host = host.split("://")[-1].split("/")[0]
		assert(host)

		port = int(port)
		assert(is_port_valid(port))

		return host, port
	except (AssertionError, AttributeError, ValueError, IndexError):
		return None, None

def is_host_ingress(host:str) -> bool:
	"""
	Checks if the given host is inbound.

	Args:
		host (str): The host to be checked. Can be an IP address or a host, and can contain a protocol and port.

	Returns:
		bool: Is host inbound
	"""
	if(host is None):
		return False

	bare_host, bare_port = try_extract_bare_host_and_port(host)
	if(bare_host):
		return (
			is_ip_loopback(bare_host)
		)
	else:
		# Extract the host part of the URL
		safe_host = host.split("://")[-1]
		safe_host = safe_host.split("/")[0]

		# safe_host now can be like:
		# localhost
		# 127.0.0.1
		# 127.0.0.1:6000
		# [2001:0000:130F:0000:0000:09C0:876A:130B]:4444
		return (
			'127.0.0.' in safe_host or
			'localhost' in safe_host or
			is_ip_loopback(safe_host)
		)
