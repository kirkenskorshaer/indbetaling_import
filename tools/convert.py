def int_tryparse(input):
	try:
		return int(input)
	except ValueError:
		return None
