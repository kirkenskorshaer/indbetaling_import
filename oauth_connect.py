import requests
import json.decoder


class OauthConnect():
	def __init__(self, config, data):
		self.config = config
		self.data = data

	def get_request_headers(self):
		self.data.create_access_token_if_needed(self.config.authorization_endpoint, self.config.base_url, self.config.application_id)
		return self._create_header_from_token(), None

	def _create_header_from_token(self):
		return {
			'Authorization': 'Bearer ' + self.data.access_token,
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
