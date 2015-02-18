""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	# Load file and remove header
	f = open(file_name,'r')
	lines = f.readlines()
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
		curr_line += 1
		lines = lines[curr_line+1:]

    # Split lines into lowercase words and add to all_words list
	all_words = []
	for line in lines:
		remove_chars = "0123456789~`!@#$%^&*()_-+={[}]|\:;'<,"">.?/"
		line = line.replace('"', '').strip()
		line = line.translate(None, remove_chars)
		line = line.lower()
		all_words.extend(line.split())

	return all_words

def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""
	# Organize words in dict by frequency
	word_counts = {}
	count = 0
	for word in word_list:
		count = word_list.count(word)
		word_counts[word] = count
		word_list.remove(word)

	# List words in list by frequency
	ordered_by_frequency = sorted(word_counts, key=word_counts.get, reverse=True)
	top_n_words = ordered_by_frequency[:n]

	return top_n_words

word_list = get_word_list('sherlock_holmes.txt')
get_top_n_words(word_list, 100)
