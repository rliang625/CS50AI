import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    running_dict = dict()
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory,filename), encoding = "utf8") as f:
                file_text = f.read()
                running_dict[filename] = file_text
    return running_dict 

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    word_list = list()
    for word in nltk.tokenize.word_tokenize(document.lower()):
        if word not in nltk.corpus.stopwords.words("english"):
            for char in word:
                no_punct = True
                if char in string.punctuation:
                    no_punct = False
                    break
                if no_punct:
                    word_list.append(word)
    return word_list

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    running_dict = dict()
    return_dict = dict()
    document_count = len(documents)
    for document in documents:
        document_words = set(documents[document])
        for word in document_words:
            if word not in running_dict:
                running_dict[word] = 1
            else:
                running_dict[word] += 1
    for word in running_dict:
        return_dict[word] = math.log(document_count/running_dict[word]) 
    return return_dict



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf_values_dict = {file:0 for file in files}
    for word in query:
        if word in idfs:
            for file in files:
                tf = files[file].count(word)
                tf_idf_values_dict[file] += (tf * idfs[word])
    return_values = sorted([file for file in files],key = lambda x : tf_idf_values_dict[x], reverse = True)[:n]    
    return return_values





def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    running_dict = dict()
    for sentence in sentences:
        running_idfs_value = 0
        query_term_count = 0
        sentence_length = len(nltk.tokenize.word_tokenize(sentence))
        for word in query:
            if word in sentence:
                running_idfs_value += idfs[word]
                query_term_count += 1
        running_dict[sentence] = (running_idfs_value,(query_term_count/sentence_length))
    return sorted([sentence for sentence in sentences], key = lambda x: running_dict[x], reverse = True)[:n]



if __name__ == "__main__":
    main()

