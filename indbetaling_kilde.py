class IndbetalingKilde(object):
	Andet = 'Andet', 170590000
	Bankoverfoersel = 'Bankoverfoersel', 100000005
	Giro = 'Giro', 100000004
	Kontant = 'Kontant', 100000000
	MobilePay = 'MobilePay', 100000001
	Sms = 'Sms', 100000002
	Swipp = 'Swipp', 100000003
	Ukendt = 'Ukendt', 100000100
	N_ = 'N', 170590002
	O_ = 'O', 170590001


def get(ntry, new_kkadmin_medlemsnr):
	kilde = IndbetalingKilde

	if ntry.BkTxCdDomnCd == "PMNT" and ntry.BkTxCdDomnFmlyCd == "MCRD" and ntry.BkTxCdDomnFmlySubFmlyCd == "POSP":
		return kilde.MobilePay

	if ntry.BkTxCdDomnCd == "PMNT" and ntry.BkTxCdDomnFmlyCd == "RCDT" and ntry.BkTxCdDomnFmlySubFmlyCd == "VCOM":
		return kilde.Giro

	if ntry.BkTxCdDomnCd == "PMNT" and ntry.BkTxCdDomnFmlyCd == "RCDT" and ntry.BkTxCdDomnFmlySubFmlyCd == "DMCT":
		return kilde.Bankoverfoersel

	if ntry.BkTxCdDomnCd == "PMNT" and ntry.BkTxCdDomnFmlyCd == "CNTR" and ntry.BkTxCdDomnFmlySubFmlyCd == "CDPT":
		return kilde.Kontant

	if new_kkadmin_medlemsnr is not None:
		return kilde.Kontant

	return kilde.Ukendt
