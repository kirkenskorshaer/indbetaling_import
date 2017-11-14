import requests
from adal import AuthenticationContext
from datetime import datetime, timedelta
import json.decoder


class OauthConnect(object):
	expires_on = None
	access_token = None
	token_in_returned_header_is_valid_for_at_least_this_many_seconds = 10

	username = None
	password = None
	config = None

	def get_request_headers(self):
		max_alowed_datetime = datetime.now() - timedelta(seconds=self.token_in_returned_header_is_valid_for_at_least_this_many_seconds)
		if self.expires_on is not None and max_alowed_datetime < self.expires_on:
			return self._create_header_from_token(), None

		return self._make_request_headers()

	def _make_request_headers(self):
		auth_context = AuthenticationContext(self.config.authorization_endpoint, api_version=None)
		token_response = auth_context.acquire_token_with_username_password(self.config.base_url, self.username, self.password, self.config.application_id)

		try:
			self.access_token = token_response['accessToken']
			self.expires_on = datetime.strptime(token_response['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
		except(KeyError):
			return None, repr(token_response)

		return self._create_header_from_token(), None

	def _create_header_from_token(self):
		return {
			'Authorization': 'Bearer ' + self.access_token,
			'OData-MaxVersion': '4.0',
			'OData-Version': '4.0',
			'Accept': 'application/json',
			'Content-Type': 'application/json; charset=utf-8;IEEE754Compatible=true',
			'Prefer': 'odata.maxpagesize=500',
			'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue',
			'Prefer': 'return=representation'
		}

	def execute_get_query(self, query):
		return self._execute_query(query, data=None, method=requests.get)

	def execute_post_query(self, query, data):
		return self._execute_query(query, data=data, method=requests.post)

	def execute_put_query(self, query, data):
		return self._execute_query(query, data=data, method=requests.put)

	def _execute_query(self, query, data, method):
		headers, header_error = self.get_request_headers()

		if headers is None:
			None, header_error

		url = self.config.api_url + query
		crm_response = None
		if data is None:
			crm_response = method(url, headers=headers)
		else:
			crm_response = method(url, json=data, headers=headers)

		crm_json = None
		try:
			crm_json = crm_response.json()
		except json.decoder.JSONDecodeError as message:
			return None, repr(crm_response)

		return crm_json, None

	def associate(self, parent_name, parent_value, child_reference_name, child_name, child_value):
		query = child_name + '(' + child_value + ')/' + child_reference_name + '/$ref'

		data = {
			'@odata.id': self.config.api_url + parent_name + '(' + parent_value + ')'
		}

		return self.execute_put_query(query, data)


connector = OauthConnect()
