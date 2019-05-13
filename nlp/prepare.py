import pandas as pd
import nltk
import acquire
import re
import unicodedata
from nltk.corpus import stopwords

def basic_clean(string):
    """Will lowercase, normalize, and remove anything that isn't a letter, number, whitespace or single quote and return it."""
    clean_string = string.lower()
    clean_string = unicodedata.normalize('NFKD', clean_string).\
                    encode('ascii', 'ignore').\
                    decode('utf-8', 'ignore')
    clean_string = re.sub(r'[^\w\s\']', '', clean_string)
    return clean_string

def tokenize(string, string_or_list='string'):
    """nltk.tokenize.ToktokTokenizer"""
    tokenizer = nltk.tokenize.ToktokTokenizer()
    if string_or_list == 'string':
        return tokenizer.tokenize(string, return_str=True)
    if string_or_list == 'list':
        return tokenizer.tokenize(string)

def stem(string, string_or_list='string'):
    """Returns the stems."""
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    stemmed_string = ' '.join(stems)
    if string_or_list == 'list':
        return stems
    if string_or_list == 'string':
        return stemmed_string

def lemmatize(string, string_or_list='string'):
    """Returns the lemmatized text."""
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    lemmatized_string = ' '.join(lemmas)
    if string_or_list == 'string':
        return lemmatized_string
    if string_or_list == 'list':
        return lemmas

def remove_stopwords(string, string_or_list='string', extra_words=None, exclude_words=None):
    """Removes the stopwords from the text then returns it. Able to add or remove stopwords."""
    stopword_list = stopwords.words('english')
    if extra_words != None:
        for word in extra_words:
            stopword_list.append(word)
    if exclude_words != None:
        for word in exclude_words:
            stopword_list.remove(word)
    filtered_words = [word for word in string.split() if word not in stopword_list]
    filtered_string = ' '.join(filtered_words)
    if string_or_list == 'string':
        return filtered_string
    if string_or_list == 'list':
        return filtered_words

def prep_article(dictionary):
    """Will return a dictionary with title, category(if available), original content, cleaned, stemmed, and lemmatized content."""
    new_dict = {}
    new_dict['title'] = dictionary['title']
    if 'category' in dictionary.keys():
        new_dict['category'] = dictionary['category']
    new_dict['original'] = dictionary['body']
    new_dict['clean'] = remove_stopwords(basic_clean(dictionary['body']))
    new_dict['stemmed'] = stem(new_dict['clean'])
    new_dict['lemmatized'] = lemmatize(new_dict['clean'])
    return new_dict

def prepare_article_data(list_of_dictionaries):
    """Returns a list of dictionaries that have been cleaned, stemmed, lemmatized, etc."""
    new_list_of_dict = []
    for dictionary in list_of_dictionaries:
        new_list_of_dict.append(prep_article(dictionary))
    return new_list_of_dict