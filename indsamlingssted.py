def get(connector, campaignid, accountid):
	if accountid is None:
		return

	query = 'nrq_indsamlingssteds?$select=nrq_indsamlingsstedid,nrq_name&$filter=_nrq_indsamlingssted_value eq ' + accountid + ' and _nrq_landsindsamling_value eq ' + campaignid + '&$top=1'

	result_json, error = connector.execute_get_query(query)
	if error is not None:
		raise ValueError(repr(error))

	try:
		name = result_json['value'][0].get('nrq_name')
		sted_id = result_json['value'][0].get('nrq_indsamlingsstedid')
		return sted_id, name
	except IndexError:
		return None, None
	except KeyError:
		raise ValueError('invalid response: ' + repr(result_json))
