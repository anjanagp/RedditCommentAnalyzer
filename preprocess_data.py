from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


porter= PorterStemmer()
stop_words = set(stopwords.words('english'))

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
        return ' '.join(preprocessed_comment)
