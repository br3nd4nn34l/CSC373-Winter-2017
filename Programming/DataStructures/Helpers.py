def add_to_dict_lst(dct, key, item):
	if key not in dct:
		dct[key] = []
	dct[key] += [item]


def safe_dict_delete(dict, key):
	try:
		del dict[key]
	except KeyError:
		pass