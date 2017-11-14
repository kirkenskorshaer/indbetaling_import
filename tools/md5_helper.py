import hashlib


def to_md5(input):
	md5 = hashlib.md5()
	md5.update(input.encode('utf-8'))
	return md5.hexdigest()


def to_dashed_md5(input):
	md5 = hashlib.md5()
	md5.update(input.encode('utf-8'))
	upper_md5 = md5.hexdigest().upper()
	dashed_md5 = ''
	added_chars_since_dash = 0
	print(upper_md5)
	for char in upper_md5:
		if added_chars_since_dash == 2:
			dashed_md5 += '-' + char
			added_chars_since_dash = 1
		else:
			dashed_md5 += char
			added_chars_since_dash += 1

	return dashed_md5
