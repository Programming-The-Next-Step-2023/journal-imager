import nltk
import numpy as np
from scipy import spatial

def get_most_surprising_words(entries, model, n_images):
    """ Given a list of journal entries, return the n most surprising words.

    Args:
        entries (list): A list of strings, each string representing a journal entry.
        model (gensim.models.keyedvectors.Word2VecKeyedVectors): embedding structure that contains keys (i.e., words) and their corresponding GloVe embeddings.

    Returns:
        list: A list of the n most surprising words.
    """

    # Download the required NLTK resources
    nltk.download('stopwords')
    nltk.download('punkt')

    # Tokenize the text, while removing punctuation and making everything lowercase
    words = []
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    for entry in entries:
        words.extend(tokenizer.tokenize(entry.lower()))

    # Filter out:
    # a) words that are not in the model's vocabulary;
    # b) stopwords
    # c) repeated words
    words = [word for word in words if word in model.key_to_index]
    words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]
    words = list(set(words))

    # If no words left, return empty list
    if len(words) == 0:
        return []

    # For each word, compute the median vector of the REST of the words,
    # and compute the cosine similarity of the word's vector with the median vector
    word_similarities = {}
    for word in words:
        avg_vector_rest = np.median([model[other_token] for other_token in words if other_token != word], axis=0)
        word_similarities[word] = 1 - spatial.distance.cosine(model[word], avg_vector_rest)

    # Get the n words with the lowest similarity
    n_words = n_images * 3 # three words per generated image resulted in the coolest images, generally
    salient_words = sorted(word_similarities.items(), key=lambda word: word[1])[:n_words]

    # Return the salient words
    return [word for word, cos_sim in salient_words]