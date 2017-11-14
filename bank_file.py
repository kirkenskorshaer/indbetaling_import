import iso_20022_document
from lxml import etree


class BankFile():
	def __init__(self, file):
		xml_file = etree.parse(file)
		self.document = iso_20022_document.Iso20022Document(xml_file)

	def __str__(self):
		return str(self.document)
