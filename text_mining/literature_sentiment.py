""" Author: Kathryn Hite
	Date: 2/25/15
	Description: Determine the average sentiment of Ancient Roman Literature over time to correlate with the ages of Roman literature.
"""

from pattern.web import *
from pattern.en import *
import pylab as pl
import string

# Set to true if the files are not downloaded, false if working offline with presaved files
online = False

def pull_text(urls, author):
	""" Pull book text from the given Gutenber url and remove the header.
		Split the text into sentences.

		url: Project Gutenberg url for input book
		returns: list of words in the book
	"""
	global online

	if online == True:
		# If in online mode, pull the text and save it to a file
		raw_text = URL(urls).download()
		f = open(author + '.txt', 'w')
		f.write(raw_text)
		f.close()
	else:
		# Read the previously downloaded files
		f = open(author + '.txt', 'r')
		raw_text = f.read()

	return raw_text

def get_average_sentiment(authors_by_age, urls_by_author):
	""" Determine the average sentiment of books from a set of countries.

		authors_by_age: dictionary of the ages of Roman literature with their prominent authors
		urls_by_author: dictionary of authors with a url for the text of a book by that author
		sentiment_dict: a dictionary of each age with the average sentiment rating for the age
	"""
	sentiment_dict = {}
	sentiment_tuple = ()
	# for each age, determine the sentiment vaule of each author's work and average the values to determine the sentiment of the age
	for age in authors_by_age:
		age_sentiment = 0
		count = 0.0
		for author in authors_by_age[age]:
			book = pull_text(urls_by_author[author], author)
			sentiment_tuple = sentiment(book)
			age_sentiment += sentiment_tuple[0]
			count +=1
		age_sentiment = age_sentiment / count
		sentiment_dict[age] = age_sentiment

	return sentiment_dict

def plot_sentiments(sentiment_dict):
	""" Plot the sentiments by age using pylab

		sentiment_dict: dictionary of sentiments by age
		returns: a plot of the average sentiment values by age
	"""
	print sentiment_dict
	# Set up figure and labels
	pl.figure(figsize=(8, 6), dpi=80)
	pl.xlim(0, 5)
	pl.ylim(-1, 1)
	pl.xticks([1, 2, 3, 4], ['Early', 'Golden', 'Augustan', 'Imperial'])
	pl.title('Sentiment of Roman Literature by Age')
	# Plot the sentiments in the figure
	pl.plot([1, 2, 3, 4], [sentiment_dict['early'], sentiment_dict['golden'], sentiment_dict['augustan'], sentiment_dict['imperial']], linewidth = 2.0)
	pl.show()

# Test selection of authors 
authors_by_age = {'early':['Plautus', 'Cato'], 
					'golden':['Cicero', 'Caesar', 'Lucretius', 'Catullus'], 
					'augustan':['Vergil', 'Horace', 'Livy', 'Ovid'], 
					'imperial':['Seneca', 'Pliny']}

urls_by_author = {'Plautus':'https://www.gutenberg.org/ebooks/7282.txt.utf-8',
					'Cato':'https://www.gutenberg.org/ebooks/12140.txt.utf-8',
					'Cicero':'https://www.gutenberg.org/files/39355/39355-0.txt',
					'Caesar':'https://www.gutenberg.org/ebooks/10657.txt.utf-8',
					'Lucretius':'https://www.gutenberg.org/ebooks/785.txt.utf-8',
					'Catullus':'https://www.gutenberg.org/files/18867/18867-0.txt',
					'Vergil':'https://www.gutenberg.org/ebooks/22456.txt.utf-8',
					'Horace':'https://www.gutenberg.org/ebooks/5419.txt.utf-8',
					'Livy':'https://www.gutenberg.org/files/19725/19725-0.txt',
					'Ovid':'https://www.gutenberg.org/ebooks/47677.txt.utf-8',
					'Seneca':'https://www.gutenberg.org/ebooks/3794.txt.utf-8',
					'Pliny':'https://www.gutenberg.org/ebooks/2811.txt.utf-8'}

plot_sentiments(get_average_sentiment(authors_by_age, urls_by_author))