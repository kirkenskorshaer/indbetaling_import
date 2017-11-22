import logging


def get_id(bank_id, connector):
	query = 'new_indbetalings?$select=new_indbetalingid&$filter=new_bankid eq \'' + bank_id + '\'&$top=1'

	result_json, error = connector.execute_get_query(query)

	if error is not None:
		raise ValueError(repr(error))

	indbetaling_id = None

	try:
		# return result_json['value'][0].get('new_indbetalingid')
		indbetaling_id = result_json['value'][0]['new_indbetalingid']
		logging.info('		(' + bank_id + ') found: ' + repr(indbetaling_id))
	except IndexError:
		logging.info('		(' + bank_id + ') not found: ' + repr(result_json))

	return indbetaling_id


def create(connector, ntry, ntry_string_number, kilde_code, indbetaling_status_code, campaign_id, sted_id, indbetaling_type_id):
	query = 'new_indbetalings?$select=new_indbetalingid'

	data = {
		'new_amount': str(ntry.Amt),
		'new_bankid': ntry.BankId,
		'new_bankkildekode': ntry.BkTxCdDomnCd + ' / ' + ntry.BkTxCdDomnFmlyCd + ' / ' + ntry.BkTxCdDomnFmlySubFmlyCd,
		'nrq_tekst': ntry.BkTxCdPrtryCd,
		'new_kilde': kilde_code,
		'new_name': 'auto oprettet indbetaling',
		'new_valdt': ntry.ValDt.strftime('%Y-%m-%d'),
		'nrq_indbetalingstatus': indbetaling_status_code
	}

	result_json, error = connector.execute_post_query(query, data)

	if error is not None:
		raise ValueError(repr(error))

	try:
		indbetaling_id = result_json['new_indbetalingid']

		logging.info('		(' + ntry_string_number + ') imported indbetaling to: ' + indbetaling_id)
	except KeyError:
		raise ValueError('invalid response: ' + repr(result_json))

	if sted_id is None:
		logging.warning('		(' + ntry_string_number + ') no indbetaling sted found')
	else:
		connector.associate('new_indbetalings', indbetaling_id, 'nrq_nrq_indsamlingssted_new_indbetaling_Indsamlingssted', 'nrq_indsamlingssteds', sted_id)

	connector.associate('new_indbetalings', indbetaling_id, 'new_campaign_indbetaling', 'campaigns', campaign_id)

	if indbetaling_type_id is None:
		logging.warning('		(' + ntry_string_number + ') no indbetalingtype found')
	else:
		connector.associate('new_indbetalings', indbetaling_id, 'nrq_nrq_indbetalingstype_new_indbetaling_Indbetalingstype', 'nrq_indbetalingstypes', indbetaling_type_id)

	return indbetaling_id
