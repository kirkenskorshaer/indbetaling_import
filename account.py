def get_from_medlemsnr(connector, new_kkadmin_medlemsnr):
	if new_kkadmin_medlemsnr is None or new_kkadmin_medlemsnr == '':
		return None, None

	query = 'accounts?$select=accountid,name&$filter=new_kkadminmedlemsnr eq ' + str(new_kkadmin_medlemsnr) + '&$top=1'

	result_json, error = connector.execute_get_query(query)
	if error is not None:
		raise ValueError(repr(error))

	try:
		name = result_json['value'][0].get('name')
		account_id = result_json['value'][0].get('accountid')
		return account_id, name
	except IndexError:
		return None, None
	except KeyError:
		raise ValueError('invalid response: ' + repr(result_json))
