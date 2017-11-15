import tools.md5_helper as md5_helper
from datetime import datetime
from decimal import Decimal
from lxml.etree import tostring


class Iso20022Ntry():
	def __init__(self, ntry, nsmap):
		self.BankId = None
		self.ValDt = None
		self.Amt = None
		self.Ccy = None
		self.Prtry = None
		self.BkTxCdDomnCd = None
		self.BkTxCdDomnFmlyCd = None
		self.BkTxCdDomnFmlySubFmlyCd = None
		self.BkTxCdPrtryCd = None
		self.NtryRef = None

		AddtlInfInd = ntry.find('AddtlInfInd', nsmap)
		bank_id = None

		if AddtlInfInd is not None:
			MsgNmId = AddtlInfInd.find('MsgNmId', nsmap)
			if MsgNmId is not None:
				bank_id = MsgNmId.text

		NtryRef = ntry.find("NtryRef", nsmap)
		if NtryRef is not None:
			self.NtryRef = int(NtryRef.text)
			NtryRef.getparent().remove(NtryRef)

		if bank_id is None:
			node_text = self._node_to_text(ntry)
			bank_id = md5_helper.to_md5(node_text)

		self.BankId = bank_id
		self.ValDt = datetime.strptime(ntry.find('ValDt/Dt', nsmap).text, '%Y-%m-%d')
		self.Amt = Decimal(ntry.find('Amt', nsmap).text)
		self.Ccy = ntry.find('Amt', nsmap).attrib['Ccy']
		NtryDtls = ntry.find('NtryDtls', nsmap)
		if NtryDtls is not None:
			TxDtls = NtryDtls.find('TxDtls', nsmap)
			if TxDtls is not None:
				Purp = TxDtls.find('Purp', nsmap)
				if Purp is not None:
					Prtry = Purp.find('Prtry', nsmap)
					if Prtry is not None:
						self.Prtry = Prtry.text
		BkTxCd = ntry.find('BkTxCd', nsmap)
		if BkTxCd is not None:
			Domn = BkTxCd.find('Domn', nsmap)
			if Domn is not None:
				Cd = Domn.find('Cd', nsmap)
				if Cd is not None:
					self.BkTxCdDomnCd = Cd.text
				Fmly = Domn.find('Fmly', nsmap)
				if Fmly is not None:
					Cd = Fmly.find('Cd', nsmap)
					if Cd is not None:
						self.BkTxCdDomnFmlyCd = Cd.text
					SubFmlyCd = Fmly.find('SubFmlyCd', nsmap)
					if SubFmlyCd is not None:
						self.BkTxCdDomnFmlySubFmlyCd = SubFmlyCd.text
			Prtry = BkTxCd.find('Prtry', nsmap)
			if Prtry is not None:
				Cd = Prtry.find('Cd', nsmap)
				if Cd is not None:
					self.BkTxCdPrtryCd = Cd.text

	def _node_to_text(self, node):
		node_text = tostring(node).decode("utf-8")
		return node_text

	def __str__(self):
		output = '	BankId: ' + repr(self.BankId) + '\n'
		output += '	ValDt: ' + repr(self.ValDt) + '\n'
		output += '	Amt: ' + repr(self.Amt) + '\n'
		output += '	Ccy: ' + repr(self.Ccy) + '\n'
		output += '	Prtry: ' + repr(self.Prtry) + '\n'
		output += '	BkTxCdDomnCd: ' + repr(self.BkTxCdDomnCd) + '\n'
		output += '	BkTxCdDomnFmlyCd: ' + repr(self.BkTxCdDomnFmlyCd) + '\n'
		output += '	BkTxCdDomnFmlySubFmlyCd: ' + repr(self.BkTxCdDomnFmlySubFmlyCd) + '\n'
		output += '	BkTxCdPrtryCd: ' + repr(self.BkTxCdPrtryCd) + '\n'

		return output
