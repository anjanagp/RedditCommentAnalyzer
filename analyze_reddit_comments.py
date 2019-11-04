#------------------------------------------------------------------------------#
# Part 1 : Using the PRAW API to collect top comments of a subreddit
# Part 2 : Create an Inverted Index to develop a Boolean Retrieval Model
# Notes : Make topic(subreddit) a command line parameter
#       : Create a class
#       : Add a function for intersection of sets to handle boolean queries
#       : Better pre-processing data, like tokenizing, etc
#------------------------------------------------------------------------------#

import praw
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# Create reddit object using praw
reddit = praw.Reddit(client_id='VznDMOLDMyeDfQ',
                    client_secret='HlWz9w2XNfPlsHHwVZv6d2nlhdQ',
                    user_agent='subSentiment')

inverted_index = {} # where key is the term and value is the postings list

def collect_top_comments(topic, no_of_submissions=10):
    """
    This function collects the top comments for the given topic(subreddit) and
    saves it into a text file.
    Args:
        topic [string] : name of subreddit (for example for /r/aww pass 'aww')
        no_of_submissions [integer] : limit on number of submissions to crawl
    Returns:
        inverted_index [dict] : a dictionary where each key is a term and the
        corresponsing value is its postings list
    """
    subreddit = reddit.subreddit(topic)
    no_of_comments_collected = 0
    with open('topComments.txt', 'w') as f:
        for submission in subreddit.hot(limit=no_of_submissions):
            submission.comments.replace_more(limit=0)
            top_level_comments = list(submission.comments)
            for comment in top_level_comments:
                terms = (comment.body).split() # list of terms
                for t in terms:
                    if t not in stop_words:
                        inverted_index.setdefault(t, [])
                        if submission.id not in inverted_index[t]:
                            inverted_index[t].append(submission.id)
                f.write(comment.body)
                no_of_comments_collected = no_of_comments_collected + 1
    return inverted_index

index = collect_top_comments(topic='joker', no_of_submissions=10)
