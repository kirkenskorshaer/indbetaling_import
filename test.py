import unittest
import bank_file
import tools.md5_helper as md5_helper


class indbetalinger_import(unittest.TestCase):
	def test_bank_id_does_not_change_if_xml_has_linebreaks(self):
		file = 'test_equal_indbetaling.xml'
		current_bank_file = bank_file.BankFile(file)
		self.assertEqual(current_bank_file.document.Ntries[1].BankId, current_bank_file.document.Ntries[2].BankId)

	def test_md5_is_equal_for_2_identical_strings(self):
		md5_1 = md5_helper.to_md5('test')
		md5_2 = md5_helper.to_md5('test')
		self.assertEqual(md5_1, md5_2)


if __name__ == '__main__':
	unittest.main()
