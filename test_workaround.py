#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
	import pytest
except (ImportError, ModuleNotFoundError):
	print("Please install prerequisite,")
	print("```")
	print("pip install pytest")
	print("```")
	exit()

from flask import Flask, request

from main import gevent_bug_workaround as wsgi_get_proxy_url

# Create a Flask app for testing
app = Flask(__name__)

def test_wsgi_get_proxy_url():
	with app.test_request_context('/http://frogfind.com/hello/?q=foobar'):
		request.url = 'http://frogfind.com/http://frogfind.com/hello/?q=foobar'
		request.host = 'frogfind.com'
		request.path = 'http://frogfind.com/hello/'
		request.query_string = b'q=foobar'

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url == 'http://frogfind.com/hello/?q=foobar'

def test_wsgi_get_proxy_url_edgecase_1():
	with app.test_request_context('/localhost:5000/'):
		request.url = 'http://localhost:5000/http://localhost:5000/'
		request.host = 'localhost:5000'
		request.path = '/'
		request.query_string = b''

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url == 'http://localhost:5000/'

def test_wsgi_get_proxy_url_edgecase_2():
	with app.test_request_context('/localhost:5000/'):
		request.url = 'https://localhost:5000/https://localhost:5000/'
		request.host = 'localhost:5000'
		request.path = '/'
		request.query_string = b''

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url == 'https://localhost:5000/'

def test_wsgi_get_proxy_url_edgecase_3():
	with app.test_request_context('/http://frogfind.com/hello/?q=foobar'):
		request.url = 'http://frogfind.com/http://frogfind.com/hello/?q=foobar'
		request.host = 'frogfind.com'
		request.path = 'http://frogfind.com/hello/'
		request.query_string = b'q=foobar'

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url == 'http://frogfind.com/hello/?q=foobar'

def test_wsgi_get_proxy_url_edgecase_4():
	with app.test_request_context('/http://frogfind.com/hello/'):
		request.url = 'http://frogfind.com/http://frogfind.com/hello/'
		request.host = 'frogfind.com'
		request.path = 'http://frogfind.com/hello/'
		request.query_string = b''

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url == 'http://frogfind.com/hello/'

def test_wsgi_get_proxy_url_edgecase_5():
	with app.test_request_context('/http://frogfind.com:5000/test o+o'):
		request.url = 'http://frogfind.com:5000/http://frogfind.com:5000/test%20o%2Bo'
		request.host = 'frogfind.com:5000'
		request.path = '/http://frogfind.com:5000/test o+o' # 'http://frogfind.com:5000/test%20o%2Bo'
		request.query_string = b''

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url in ['http://frogfind.com:5000/test o+o', 'http://frogfind.com:5000/test%20o%2Bo']

def test_wsgi_get_proxy_url_edgecase_6_urlEncode():
	with app.test_request_context('/http://frogfind.com:5000/test%20o%2Bo'):
		request.url = 'http://frogfind.com:5000/http://frogfind.com:5000/test%20o%2Bo'
		request.host = 'frogfind.com:5000'
		request.path = '/http://frogfind.com:5000/test o+o'
		request.query_string = b''

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url in ['http://frogfind.com:5000/test o+o', 'http://frogfind.com:5000/test%20o%2Bo']

def test_wsgi_get_proxy_url_edgecase_7_nonANSI():
	with app.test_request_context('/http://frogfind.com:5000/Тестування%20api'):
		request.url = 'http://frogfind.com:5000/http://frogfind.com:5000/Тестування%20api'
		request.host = 'frogfind.com:5000'
		request.path = '/http://frogfind.com:5000/Тестування api'
		request.query_string = b''

		# Call the function and get the corrected URL
		corrected_url = wsgi_get_proxy_url(request)

		# Assert the corrected URL matches the expected URL
		assert corrected_url in ['http://frogfind.com:5000/Тестування%20api', 'http://frogfind.com:5000/Тестування api']

if __name__ == '__main__':
	pytest.main(args=['-v'])
