def prefix_dict():
	f = open('/usr/share/dict/words', 'r')
	for line in f:
		print line

prefix_dict()