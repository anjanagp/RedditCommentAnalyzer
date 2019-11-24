





class Fetcher:
    def __init__(self, reddit_object):
        self.reddit = reddit_object
        self.submission_ids = []
        self.comment_id_storage = {}

    def get_top_submission_ids(self, sub, no_of_submissions=10):
        """
        This function collects the top submissions for the given subreddit
        Args:
            sub [string] : name of subreddit (for example for /r/aww pass 'aww')
            no_of_submissions [integer] : limit on number of submissions to crawl
        Returns:
            list of submission ids
        """
        subreddit = self.reddit.subreddit(sub)
        for submission in subreddit.hot(limit=no_of_submissions):
            self.submission_ids.append(submission.id)
        return self.submission_ids

    def get_submission_text(self, submission_id):
        """
        This function returns the submission title for the given
        submission id
        Returns:
            submission text
        """
        submission = self.reddit.submission(id= submission_id)
        return submission.title

    def get_submission_comment_ids(self, submission_id):
        """
        Fetches all the top level comments for the given submission id
        Also populates comment_id_storage
        Args:
            submission_id
        Returns:
            list of comment ids
        """
        submission = self.reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=0)
        top_comment_ids = list(submission.comments)
        self.comment_id_storage[submission_id] = top_comment_ids
        return top_comment_ids
