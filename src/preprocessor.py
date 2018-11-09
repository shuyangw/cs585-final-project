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

    def __init__(self, target_subreddit=None, break_limit):
        self.target_subreddit = target_subreddit
        self.break_limit = break_limit
		self.vocab = {}

    def proocess(self):
        f_name = 'RC_2015-01'
		f = open(f_name, 'r')
		out = open('out.json', 'w+')

		pure_out = open('pure_out.json', 'w+')
		s = {}
		line_count = 0
		sizecounter = 0
		sizecounter += os.stat(f_name).st_size
		#karma_averages["akali"] = average karma of comments with "akali" - good
		#number of times in unique comments["akali"] = n unique comments have this word - good
		#word_counts["akali"] = total count of "akali" in corpus - good

		try:
			with tqdm(total=sizecounter,
					unit='B', unit_scale=True, unit_divisor=1024) as pbar:
				with open(f_name, 'rb') as fh:
					for line in fh:
						comment = json.loads(line)
						comment_as_dict = dict(comment)

						subreddit = comment_as_dict['subreddit']
						if(subreddit == self.target_subreddit):
							score = int(comment_as_dict['ups'])-int(comment_as_dict['down'])
							body = comment_as_dict['body']
							for words in body.split():
								comment_word_set = {}
								if(words not in comment_word_set):
									comment_word_set[words] = 1
									#karma_averages["akali"] = average karma of comments with "akali"
									#number of times in unique comments["akali"] = n unique comments have this word
								if(words not in self.vocab):
									self.vocab[words] = 1
								else:
									self.vocab[words]+=1
						# body = comment_as_dict['body']
						# ups = comment_as_dict['ups']
						# downs = comment_as_dict['downs']
						# gilded = comment_as_dict['gilded']
						# d = {}
						# d['body'] = body
						# d['subreddit'] = subreddit
						# d['ups'] = ups
						# d['down'] = downs
						# d['gilded'] = gilded
						# json.dump(d, pure_out, indent=4, separators=(',', ': '))
						line_count += 1

						if line_count > self.break_limit:
							break

						if line:
							pbar.set_postfix(file=f_name[-10:], refresh=False)
							pbar.update(sys.getsizeof(line))
		except:
			pass

		f.close()
		sorted_by_value = sorted(s.items(), key=lambda kv: kv[1])
		print(sorted_by_value)
		print(len(s))