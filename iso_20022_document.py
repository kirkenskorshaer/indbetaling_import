from decimal import Decimal
import iso_20022_ntry


class Iso20022Document():
	def __init__(self, xml_file):
		self.IBAN = None
		self.TtlNetNtryAmt = None
		self.NbOfNtries = None
		self.Ntries = []

		namespace53 = '{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Document'
		namespace54 = '{urn:iso:std:iso:20022:tech:xsd:camt.054.001.02}Document'

		root = xml_file.getroot()
		xml_tag = root.tag
		nsmap = root.nsmap

		if xml_tag == namespace53:
			stmt = xml_file.find('BkToCstmrStmt/Stmt', nsmap)
			self.IBAN = stmt.find('Acct/Id/IBAN', nsmap).text
			ntrys = stmt.findall('Ntry', nsmap)
			self.TtlNetNtryAmt = Decimal(stmt.find('TxsSummry/TtlNtries/TtlNetNtryAmt', nsmap).text)
		elif xml_tag == namespace54:
			ntfctn = xml_file.find('BkToCstmrDbtCdtNtfctn/Ntfctn', nsmap)
			self.IBAN = ntfctn.find('Acct/Id/IBAN', nsmap).text
			ntrys = ntfctn.findall('Ntry', nsmap)
			self.TtlNetNtryAmt = Decimal(ntfctn.find('TxsSummry/TtlNtries/TtlNetNtryAmt', nsmap).text)
		else:
			raise ValueError('unknown namespace ' + xml_tag)

		for ntry in ntrys:
			current_ntry = iso_20022_ntry.Iso20022Ntry(ntry, nsmap)
			self.Ntries.append(current_ntry)

	def __str__(self):
		output = 'IBAN: ' + repr(self.IBAN)
		output += 'TtlNetNtryAmt: ' + repr(self.TtlNetNtryAmt)
		for ntry in self.Ntries:
			output += str(ntry) + '\n'

		return output
