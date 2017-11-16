class ConfigData():
	production = None
	token_endpoint = "https://login.microsoftonline.com/867f533d-343a-47e6-a16c-1e928b5763d6/oauth2/token"
	authorization_endpoint = 'https://login.microsoftonline.com/867f533d-343a-47e6-a16c-1e928b5763d6'
	application_id = '7a501885-24db-467c-94c4-c47a65bce0a0'
	api_url = None
	base_url = None

	xml_unused_path = 'xml_unused'
	xml_used_path = 'xml_used'

	only_import = None

	landsindsamling_campaign_id = '572D74BA-0FBD-E611-8101-001C42FD47A5'
	landsindsamling_konto_id = 'B1F6880F-33B0-E711-8126-70106FA6E4C1'
	landsindsamling_indbetaling_type_id = '845D6AD9-32B0-E711-8126-70106FA6E4C1'
	indbetaling_status_code = 170590003

	login_user = 'dbi@kirkenskorshaer.dk'

	threads = 25

	def __init__(self):
		production_j_n = input('Produktion y/n (n)')

		if production_j_n == 'y':
			self.api_url = "https://kkh.api.crm4.dynamics.com/api/data/v8.2/"
			self.base_url = "https://kkh.crm4.dynamics.com"
		else:
			self.api_url = "https://kkhdev.api.crm4.dynamics.com/api/data/v8.2/"
			self.base_url = "https://kkhdev.crm4.dynamics.com"
