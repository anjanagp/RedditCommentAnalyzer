# RedditCommentAnalyzer

To run the script analyze_reddit_comments.py run the following command -
  python3 analyze_reddit_comments.py subreddit
where subreddit is the name of the subreddit that needs to be analyzed.
For example for the subreddit /r/aww, pass aww as the subreddit argument.
Also ensure your python env contains the packages praw and nltk.

[Use the PRAW API to collect top comments from a subreddit]

[Create a Boolean Retrieval Model, to handle Boolean Queries]

  This is done by creating an inverted index structure which is unrivaled for
  ad hoc text search. To avoid linearly scanning documents, we index the
  documents in advance. In this case documents are equivalent to submissions.
  We view each document as a set of words and create a
  dictionary of terms and postings lists. Each word (term) is mapped to a list
  containing the IDs of the submissions it belongs to.

  All stopwords are not included in the inverted index. We also make sure all
  the submission IDs in each postings list is unique. Since the goal is a
  boolean model, we are mainly concerned with whether a term is present in a
  submission or not.

  The goal is ad hoc retrieval where we aim to provide the relevant submissions
  for a one-off user query. The query is in the form of a Boolean expression of
  terms.  
