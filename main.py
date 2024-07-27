#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Proof of Concept of a bug present in Gevent but not Flask
"""

from flask import Flask, request, render_template_string, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

import argparse
parser = argparse.ArgumentParser(description='Run the app with Flask or Gevent.')
parser.add_argument('--server', '-s', choices=['flask', 'gevent'], default='gevent', help='Choose the server to run the app.')

from networking import is_host_egress
import urllib.parse


def gevent_bug_workaround(flask_request) -> str:
	"""
	Bypass proxy URL mishandling bug and get the pre-formatted URL.
	Expected: http://frogfind.com/hello/?q=foobar
	Reality: http://frogfind.com/http://frogfind.com/hello/?q=foobar
	This function fixes this.

	Args:
		flask_request: The Flask request object containing the URL and other request data.

	Returns:
		str: The corrected proxy URL.
	"""

	# Get the default URL from the Flask request
	proxy_url = flask_request.url

	# Raise an error if no URL is found in the request
	if not proxy_url:
		raise ValueError("No URL in the WSGI request")

	# Extract the scheme (http or https) from the URL
	scheme = proxy_url.split("://")[0].lstrip("/")
	# Extract the host part of the URL
	safe_host = flask_request.host.split("://")[-1]
	safe_host = safe_host.split("/")[0]
	# Construct the base URL that should not repeat
	base_url = f"{scheme}://{safe_host}/"
	# get short URL path after the base
	url_path_short = flask_request.path.split(base_url)[-1]
	# If url_path_short is de-facto empty, then it is empty
	if(url_path_short == "/"): url_path_short = ""
	# Split the proxy URL using the base URL
	proxy_url_split = proxy_url.split(base_url)

	# Construct the presumably correct URL from the path, short URL path, and query string
	presumably_correct_url = base_url + url_path_short
	if(flask_request.query_string):
		presumably_correct_url = presumably_correct_url + "?" + flask_request.query_string.decode()

	# Check if the URL is bugged (repeated base URL or incorrect URL)
	if((len(proxy_url_split) >= 3 and (proxy_url_split[0] == proxy_url_split[1] == False)) or proxy_url != presumably_correct_url): # Bugged WSGI server
		logging.debug("*wsgi_get_proxy_url - URL was corrected!")
		logging.debug("*wsgi_get_proxy_url - old: "+proxy_url)
		# Correct the proxy URL by removing the repeated base URL
		proxy_url = base_url + proxy_url_split[-1]
		proxy_url = urllib.parse.unquote(proxy_url)
		logging.debug("*wsgi_get_proxy_url - new: "+proxy_url)
		# Sanity check to ensure the corrected URL matches the presumably correct URL
		# Sanity check is for further development:
		if(proxy_url != presumably_correct_url):
			raise ValueError(f"*wsgi_get_proxy_url fixable URLs do not match: \r\n1:{proxy_url}\r\n2:{presumably_correct_url}")

	return proxy_url


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def display_info(path):
	is_proxy_requested = is_host_egress(request.host)

	if is_proxy_requested:
		proxy_url = gevent_bug_workaround(request)
		urls_match = request.url == proxy_url
		match_text = '<font color="green">No bug: request.url is OK</font>' if urls_match else '<font color="red">BUG: request.url is incorrect</font>'

		html_content = f"""
		<html>
		<body>
			<h1>Gevent bug PoC (TAbdiukov)</h1>
			<h2>Request Information</h2>
			<p><strong>WSGI app:</strong> {args.server}</p>
			<p><strong>request.url:</strong> {request.url}</p>
			<p><strong>workaround url:</strong> {proxy_url}</p>
			<p><strong>status:</strong> {match_text}</p>
		</body>
		</html>
		"""
		return html_content.encode("mac_roman"), 200
	else:
		return "Request is not proxy", 404

if __name__ == '__main__':
	args = parser.parse_args()

	if args.server == 'flask':
		# Flask
		app.run(host="0.0.0.0", port=5000, debug=True)
	else:
		# Gevent
		http_server = WSGIServer(("0.0.0.0", 5000), app)
		http_server.serve_forever()
