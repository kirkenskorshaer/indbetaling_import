import iso_20022_document
from lxml import etree


class BankFile():
	def __init__(self, file):
		parser = etree.XMLParser(remove_blank_text=True)
		xml_file = etree.parse(file, parser=parser)
		self.document = iso_20022_document.Iso20022Document(xml_file)

	def __str__(self):
		return str(self.document)
