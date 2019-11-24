#------------------------------------------------------------------------------#
# Part 1 : Using the PRAW API to collect top comments of a subreddit
# Part 2 : Create an Inverted Index to develop a Boolean Retrieval Model
# Notes
#       : Add error handling for invalid Command Line arg
#       : Add a function for intersection of sets to handle boolean queries
#       : Use NoSQL MongoDB to store inverted index
#------------------------------------------------------------------------------#
import sys
import pprint
from pymongo import MongoClient
import fetch_data
import preprocess_data
import os
import praw

# Create reddit object using praw
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                    client_secret=os.getenv('CLIENT_SECRET'),
                    user_agent='subSentiment')

class MongoDB:
    def __init__(self, db_name):
        self.client = MongoClient()
        self.db =  self.client[db_name]

    def create_collection(self, name):
        """
        Creates a collection with the db database
        """
        return self.db[name]

    def create_post(self, post, ids, fetcher_object, storage_object, preprocess_object, collection):
        """
        """
        post["submission_id"] = ids
        post["title"] = fetcher_object.get_submission_text(ids)
        list_of_top_comments_for_sub = storage_object[ids]
        for j in range(len(list_of_top_comments_for_sub)):
            key_j = 'comment_{}'.format(j)  # a string depending on j
            post[key_j] = preprocess_object.remove_stop_words(list_of_top_comments_for_sub[j])
        db.insert_doc(db, collection, post)
        post.clear()

    def insert_doc(self, db, collection, post):
        """
        """
        collection.update(post, post, upsert=True)

    def query_doc(self, collection):
        """
        """
        collection.create_index([("$**", 'text')])
        cursor = (collection.find(
                    {"$text": {"$search": " \"puma\""}},  ## is there a way to get search for the exact word, for example in this case it looks like it'll find dog or dogs or dogshelter - but this is because tokenizes and stems the search term(s) so its good no need to change
                    {"score": {'$meta': "textScore"}}).sort([('score', {'$meta': 'textScore'})])).limit(5)
        for doc in cursor:
            print(doc.get('score'))
            print (doc.get('_id'))

# Get the list of submission ids and add each submission id, title and comments
# into each document
fetcher_object = fetch_data.Fetcher(reddit)
fetcher_object.get_top_submission_ids(sub= sys.argv[1], no_of_submissions=2)
[fetcher_object.get_submission_comment_ids(sub_id) for sub_id in fetcher_object.submission_ids]
storage_object = fetcher_object.comment_id_storage

# Create a db and collection to store all the submissions
# Adds each submission with its info into a new document in the collection
db = MongoDB(db_name='reddit_submission_data')
collection = db.create_collection('submission_info_collection')

preprocess_object = preprocess_data.PreprocessData()
collection.drop() # gets rid of previous values. if want to append, take care that same submission_ids are not added since the comments change

for ids in fetcher_object.submission_ids:
    db.create_post({}, ids, fetcher_object, storage_object, preprocess_object, collection)

# #query indexing
db.query_doc(collection)
