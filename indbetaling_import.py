import os
import getpass
import bank_file
import config_data
import oauth_connect
import indbetaling
import account
import indsamlingssted
import indbetaling_kilde
import tools.convert as convert
import logging
import datetime


class IndbetalingImport():
	def indbetaling_import(self):
		config = config_data.ConfigData()
		self._set_log()

		files = os.listdir(config.xml_unused_path)

		if len(files) == 0:
			return True

		connector = oauth_connect.connector
		# connector.username = input('username: ')
		connector.username = config.login_user
		connector.password = getpass.getpass('password: ')
		connector.config = config

		for file in files:
			current_bank_file = bank_file.BankFile(config.xml_unused_path + '/' + file)
			iso20022_document = current_bank_file.document

			logging.info(str(iso20022_document.IBAN) + ' - ' + repr(iso20022_document.NbOfNtries) + ' - ' + str(iso20022_document.TtlNetNtryAmt) + ' - ' + file)

			for ntry in iso20022_document.Ntries:
				self._import_ntry(ntry, iso20022_document, config, connector)

			# os.rename(config.xml_unused_path + '/' + file, config.xml_used_path + '/' + file)

	def _set_log(self):
		logging.basicConfig(filename='log/' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.log', level=logging.DEBUG, datefmt='%H:%M:%S')
		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		formatter = logging.Formatter('%(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)

	def _import_ntry(self, ntry, iso20022_document, config, connector):
		if config.only_import is not None and ntry.BankId not in config.only_import:
			return

		existing_indbetaling_id = indbetaling.get_id(ntry.BankId, connector)
		ntry_string_number = repr(ntry.NtryRef) + ' / ' + repr(iso20022_document.NbOfNtries)

		if existing_indbetaling_id is not None:
			logging.info('	(' + ntry_string_number + ') indbetaling already exists: ' + ntry.BankId + ' value: ' + str(ntry.Amt))
			return

		logging.info('	(' + ntry_string_number + ')importing: ' + ntry.BankId + ' value: ' + str(ntry.Amt))

		new_kkadmin_medlemsnr = convert.int_tryparse(ntry.BkTxCdPrtryCd)

		if new_kkadmin_medlemsnr is None:
			logging.info('		medlemsnr not found')
		else:
			logging.info('		medlemsnr: ' + str(new_kkadmin_medlemsnr))

		kilde_name, kilde_code = indbetaling_kilde.get(ntry, new_kkadmin_medlemsnr)
		logging.info('		' + repr(kilde_name))

		account_id, account_name = account.get_from_medlemsnr(connector, new_kkadmin_medlemsnr)
		campaign_id = config.landsindsamling_campaign_id
		indbetaling_type_id = config.landsindsamling_indbetaling_type_id
		indbetaling_status_code = config.indbetaling_status_code

		sted_id = None
		if account_id is not None:
			logging.info('		account: ' + account_name + ' (' + account_id + ')')
			sted_id, sted_name = indsamlingssted.get(connector, campaign_id, account_id)
			if sted_id is not None:
				logging.info('		stedid: ' + sted_name + ' (' + sted_id + ')')

		indbetaling.create(connector, ntry, kilde_code, indbetaling_status_code, campaign_id, sted_id, indbetaling_type_id)


if __name__ == "__main__":
	IndbetalingImport().indbetaling_import()
