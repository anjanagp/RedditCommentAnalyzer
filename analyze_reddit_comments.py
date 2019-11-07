#------------------------------------------------------------------------------#
# Part 1 : Using the PRAW API to collect top comments of a subreddit
# Part 2 : Create an Inverted Index to develop a Boolean Retrieval Model
# Notes
#       : Add error handling for invalid Command Line arg
#       : Add a function for intersection of sets to handle boolean queries
#       : Use NoSQL MongoDB to store inverted index
#------------------------------------------------------------------------------#
import os
import sys
import praw
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
porter= PorterStemmer()
stop_words = set(stopwords.words('english'))

# Create reddit object using praw
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                    client_secret=os.getenv('CLIENT_SECRET'),
                    user_agent='subSentiment')

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
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.hot(limit=no_of_submissions):
            self.submission_ids.append(submission.id)
        return self.submission_ids

    def get_submission_comment_ids(self, submission_id):
        """
        Fetches all the top level comments for the given submission id
        Also populates comment_id_storage
        Args:
            submission_id
        Returns:
            list of comment ids
        """
        submission = reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=0)
        top_comment_ids = list(submission.comments)
        self.comment_id_storage[submission_id] = top_comment_ids
        return top_comment_ids

class PreprocessData:

    def remove_stop_words(self, comment_id):
        """
        Removes all stop words from data and tokenizes it
        Returns a list of preprocessed terms derived from the comment
        Args:
            comment_id
        """
        preprocessed_comment = []
        tokens = word_tokenize(comment_id.body)
        words = [word for word in tokens if word.isalpha()]
        for w in words:
            if not w in stop_words:
                preprocessed_comment.append(porter.stem(w))
        return preprocessed_comment

class Inverted_Index:
    def __init__(self):
        self.index = dict()

    def index_comment(self, submission_id, comment_list):
        """
        Indexes a comment list by populating the index where they key is the
        submission_id and the value is a postings list which contains all the
        terms that belong to that submission_id
        Args:
            submission_id
            comment_list
        """
        for comment in comment_list:
            for term in comment:
                self.index.setdefault(term, [])
                if submission_id not in self.index[term]:
                    self.index[term].append(submission_id)
        return self.index

    def lookup_query(self, query):
        """
        """
        # take a boolean query and return the list of correct submission ID
        print("Not implemented")

# Fetch data
fetcher_object = Fetcher(reddit)
list_of_ids = fetcher_object.get_top_submission_ids(sub= sys.argv[1], no_of_submissions=1)
for i in list_of_ids:
    fetcher_object.get_submission_comment_ids(i)
storage_object = fetcher_object.comment_id_storage
preprocess_object = PreprocessData()
# Preprocess data
for k, v in storage_object.items():
    temp = []
    for comment_id in v:
        temp.append(preprocess_object.remove_stop_words(comment_id))
    storage_object[k] = temp
# Create Inverted Index
final_index = Inverted_Index()
for k,v in storage_object.items():
    final_index.index_comment(k, v)

final_index.index.update({k: sorted(v) for k, v in final_index.index.items()}) # sorting postings list in ascending order of submission ID
print("inverted index is ", final_index.index)
