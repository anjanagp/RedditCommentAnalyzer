#-------------------------x-------------------------x--------------------------x
# Part 1 : Using the PRAW API to collect top comments of a subreddit and
#          analyze them
# Notes : Make topic(subreddit) a command line parameter
#       : Create a class
#--------------------------x-----------------------x---------------------------x

import praw

# Create reddit object using praw
reddit = praw.Reddit(client_id='VznDMOLDMyeDfQ',
                    client_secret='HlWz9w2XNfPlsHHwVZv6d2nlhdQ',
                    user_agent='subSentiment')

def collect_top_comments(topic, no_of_submissions=10):
    """
    This function collects the top comments for the given topic(subreddit) and
    saves it into a text file.
    Args:
        topic [string] : name of subreddit (for example for /r/aww pass 'aww')
        no_of_submissions [integer] : limit on number of submissions to crawl
    Returns:
        no_of_comments_collected [integer] : total number of comments collected
    """
    subreddit = reddit.subreddit(topic)
    no_of_comments_collected = 0
    with open('topComments.txt', 'w') as f:
        for submission in subreddit.hot(limit=no_of_submissions):
            submission.comments.replace_more(limit=0)
            top_level_comments = list(submission.comments)
            for comment in top_level_comments:
                f.write(comment.body)
                no_of_comments_collected = no_of_comments_collected + 1
    return no_of_comments_collected

no_of_comments = collect_top_comments(topic='joker', no_of_submissions=50)
print("Total number of comments collected : ", no_of_comments)
