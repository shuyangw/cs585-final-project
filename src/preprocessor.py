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
        self.break_limit

    def proocess(self):
        pass