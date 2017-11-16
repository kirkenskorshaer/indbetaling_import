import os
import getpass
import bank_file
import config_data
import oauth_connect
import oauth_common_data
import indbetaling
import account
import indsamlingssted
import indbetaling_kilde
import tools.convert as convert
import logging
import datetime
import copy
import threading
import time


class IndbetalingImport():
	def indbetaling_import(self):
		begin_all = datetime.datetime.now()
		config = config_data.ConfigData()
		self._set_log()
		self.threads = []

		files = os.listdir(config.xml_unused_path)

		if len(files) == 0:
			return True

		connector_data = oauth_common_data.OauthCommonData()
		connector_data.username = config.login_user
		connector_data.password = getpass.getpass('password: ')

		for file in files:
			self._import_file(config, connector_data, file)

		total_time = datetime.datetime.now() - begin_all

		logging.info('completed all files in: ' + str(total_time) + ' with ' + str(config.threads) + ' thread(s)')

	def _import_file(self, config, connector_data, file):
		begin_file = datetime.datetime.now()
		current_bank_file = bank_file.BankFile(config.xml_unused_path + '/' + file)
		iso20022_document = current_bank_file.document

		logging.info(str(iso20022_document.IBAN) + ' - ' + repr(iso20022_document.NbOfNtries) + ' - ' + str(iso20022_document.TtlNetNtryAmt) + ' - ' + file)

		tasks = []
		for ntry in iso20022_document.Ntries:
			ntry_copy = copy.deepcopy(ntry)
			tasks.append([ntry_copy, iso20022_document, config, connector_data])

		while len(tasks) > 0:
			if len(self.threads) < config.threads:
				args = tasks[0]
				tasks.remove(args)
				thread = threading.Thread(target=self._import_ntry, args=args)
				self.threads.append(thread)
				thread.start()
			else:
				time.sleep(1)

			for thread in self.threads:
				if thread.is_alive() is False:
					self.threads.remove(thread)

		while len(self.threads) > 0:
			for thread in self.threads:
				if thread.is_alive() is False:
					self.threads.remove(thread)
			time.sleep(1)

		file_time = datetime.datetime.now() - begin_file
		logging.info('	completed ' + file + ' in: ' + str(file_time) + ' with ' + str(config.threads) + ' thread(s)')

		os.rename(config.xml_unused_path + '/' + file, config.xml_used_path + '/' + file)

	def _set_log(self):
		logging.basicConfig(filename='log/' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.log', level=logging.DEBUG, datefmt='%H:%M:%S')
		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		formatter = logging.Formatter('%(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)

	def _import_ntry(self, ntry, iso20022_document, config, connector_data):
		if config.only_import is not None and ntry.BankId not in config.only_import:
			return

		connector = oauth_connect.OauthConnect(config, connector_data)

		existing_indbetaling_id = indbetaling.get_id(ntry.BankId, connector)
		ntry_string_number = repr(ntry.NtryRef) + ' / ' + repr(iso20022_document.NbOfNtries)

		if existing_indbetaling_id is not None:
			logging.info('	(' + ntry_string_number + ') indbetaling already exists: ' + ntry.BankId + ' value: ' + str(ntry.Amt))
			return

		logging.info('	(' + ntry_string_number + ') importing: ' + ntry.BankId + ' value: ' + str(ntry.Amt))

		new_kkadmin_medlemsnr = convert.int_tryparse(ntry.BkTxCdPrtryCd)

		if new_kkadmin_medlemsnr is None:
			logging.info('		(' + ntry_string_number + ') medlemsnr not found')
		else:
			logging.info('		(' + ntry_string_number + ') medlemsnr: ' + str(new_kkadmin_medlemsnr))

		kilde_name, kilde_code = indbetaling_kilde.get(ntry, new_kkadmin_medlemsnr)
		logging.info('		(' + ntry_string_number + ') ' + repr(kilde_name))

		account_id, account_name = account.get_from_medlemsnr(connector, new_kkadmin_medlemsnr)
		campaign_id = config.landsindsamling_campaign_id
		indbetaling_type_id = config.landsindsamling_indbetaling_type_id
		indbetaling_status_code = config.indbetaling_status_code

		sted_id = None
		if account_id is not None:
			logging.info('		(' + ntry_string_number + ') account: ' + account_name + ' (' + account_id + ')')
			sted_id, sted_name = indsamlingssted.get(connector, campaign_id, account_id)
			if sted_id is not None:
				logging.info('		(' + ntry_string_number + ') stedid: ' + sted_name + ' (' + sted_id + ')')

		indbetaling.create(connector, ntry, ntry_string_number, kilde_code, indbetaling_status_code, campaign_id, sted_id, indbetaling_type_id)


if __name__ == "__main__":
	IndbetalingImport().indbetaling_import()
