import os
from tqdm import tqdm
import json
import sys

class Preprocessor(object):
	"""
	This is the class that will perform all of the necessary preprocessing on
	the data.

	The constructor has arguments:
	 - target_subreddit: A string that represents the subreddit we wish to
	   focus. If it is none, then we collect data on every subreddit, which
	   we do not recommend at the moment.
	 - break_limit: An int that represents the number of comments we wish to
	   collect before we stop.
	"""
	############################################################################
	# NOTE: Refer to stream.py for implementation motivation                   #
	############################################################################

	def __init__(self, target_subreddit, break_limit, threshold):
		self.target_subreddit = target_subreddit
		self.break_limit = break_limit
		self.threshold = threshold
		# self.vocab = {}

	def process(self):
		f_name = '../RC_2015-01'
		f = open(f_name, 'r')
		out = open('out.json', 'w+')

		pure_out = open('pure_out.json', 'w+')
		line_count = 0
		sizecounter = 0
		sizecounter += os.stat(f_name).st_size
		comments_of_sub = []
		with tqdm(total=sizecounter,
				unit='B', unit_scale=True, unit_divisor=1024) as pbar:
			with open(f_name, 'rb') as fh:
				for line in fh:
					comment = json.loads(line)
					comment_as_dict = dict(comment)

					subreddit = comment_as_dict['subreddit']
					if(subreddit == self.target_subreddit):
						score = int(comment_as_dict['ups'])
						comments_of_sub.append((comment_as_dict['body'], score))
						# body = comment_as_dict['body'] 
						# for words in body.split():
						# 	comment_word_set = {}
						# 	if(words not in comment_word_set):
						# 		comment_word_set[words] = 1
						# 	if(words not in self.vocab):
						# 		self.vocab[words] = 1
						# 	else:
						# 		self.vocab[words]+=1
					line_count += 1

					if line_count > self.break_limit:
						break

					if line:
						pbar.set_postfix(file=f_name[-10:], refresh=False)
						pbar.update(sys.getsizeof(line))

		f.close()
		return comments_of_sub

	def statistics(self, comments):
		import numpy as np

		scores = []
		for comment in comments:
			scores.append(comment[1])
		scores = np.array(scores)
		lower_bound = np.percentile(scores, self.threshold)

		good_comments = []
		for comment in comments:
			if comment[1] > lower_bound:
				good_comments.append(comment)
		return good_comments


p = Preprocessor("leagueoflegends", 1e7, 75)
comments = p.process()
good = p.statistics(comments)
print(good)
print(len(good))
print(len(comments))