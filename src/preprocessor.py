import os
from tqdm import tqdm
import json
import sys
import numpy as np

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

	def __init__(self, target_subreddit, break_limit, threshold, custom_file="",
		custom=False
	):
		self.target_subreddit = target_subreddit
		self.break_limit = break_limit
		self.threshold = threshold

	def process(self, custom_file="", custom=False):
		print("Processing file...")

		f_name = '../RC_2015-01'
		if custom:
			f_name = custom_file

		try:
			f = open(f_name, 'r')
		except:
			print("File not found!")
			sys.exit()

		line_count = 0
		sizecounter = 0
		sizecounter += os.stat(f_name).st_size
		output = []
		with tqdm(total=sizecounter,
				unit='B', unit_scale=True, unit_divisor=1024) as pbar:
			with open(f_name, 'r') as fh:
				if custom:
					for line in fh:
						output.append(line)
						if line:
							pbar.set_postfix(file=f_name[-10:], refresh=False)
							pbar.update(sys.getsizeof(line))
				else:
					for line in fh:
						comment = json.loads(line)
						comment_as_dict = dict(comment)
						subreddit = comment_as_dict['subreddit']
						if(subreddit == self.target_subreddit):
							score = int(comment_as_dict['ups'])
							output.append((comment_as_dict['body'], score))
						line_count += 1
						if self.break_limit != None:
							if line_count > self.break_limit:
								break
						if line:
							pbar.set_postfix(file=f_name[-10:], refresh=False)
							pbar.update(sys.getsizeof(line))

		f.close()

		print("Finished processing")
		return output, line_count

	def statistics(self, comments):
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

"""
Example of usage

p = Preprocessor("leagueoflegends", 1e7, 75)
comments = p.process()
out = open('out.txt', 'w+', encoding='utf-8')
for c in comments:
	out.write(c[0])
out.close()
good = p.statistics(comments)
print(good)
print(len(good))
print(len(comments))
"""