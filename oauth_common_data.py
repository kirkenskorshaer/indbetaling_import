import threading
from adal import AuthenticationContext
from datetime import datetime, timedelta


class OauthCommonData():
	token_in_returned_header_is_valid_for_at_least_this_many_seconds = 10

	def __init__(self):
		self.expires_on = None
		self.access_token = None

		self.username = None
		self.password = None

		self.lock = threading.Lock()

	def create_access_token_if_needed(self, authorization_endpoint, base_url, application_id):
		try:
			self.lock.acquire()
			max_alowed_datetime = datetime.now() - timedelta(seconds=self.token_in_returned_header_is_valid_for_at_least_this_many_seconds)
			if self.expires_on is not None and max_alowed_datetime < self.expires_on:
				return

			auth_context = AuthenticationContext(authorization_endpoint, api_version=None)
			token_response = auth_context.acquire_token_with_username_password(base_url, self.username, self.password, application_id)

			self.access_token = token_response['accessToken']
			self.expires_on = datetime.strptime(token_response['expiresOn'], '%Y-%m-%d %H:%M:%S.%f')
		except(KeyError):
			return None, repr(token_response)
		finally:
			self.lock.release()
