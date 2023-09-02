"""
Matching Algorithm between phonemes and facial expressions
(English language only)
"""
import nltk
from nltk.corpus import cmudict

# Necessary downloads for the CMU Pronouncing Dictionary
nltk.download('cmudict')
nltk.download('punkt')
# Initialize the CMU Pronouncing Dictionary
prondict = cmudict.dict()

# This is a mapping from phonemes to lower face numbers
# see http://www.speech.cs.cmu.edu/cgi-bin/cmudict
# Phoneme  lower face # Example
mapping = {
    'AA': 0, # odd
    'AE': 3, # at
    'AH': 3, # hut
    'AO': 4, # ought
    'AW': 2, # cow
    'AY': 2, # hide
    'B': 0, # be
    'CH': 5, # cheese
    'D': 5, # dee
    'DH': 5, # thee
    'EH': 1, # Ed
    'ER': 2, # hurt
    'EY': 2, # ate
    'F': 7, # fee
    'G': 0, # green
    'HH': 0, # he
    'IH': 2, # it
    'IY': 2, # eat
    'JH': 0, # gee
    'K': 0, # key
    'L': 0, # lee
    'M': 0, # me
    'N': 0, # knee
    'NG': 0, # ping
    'OW': 4, # oat
    'OY': 4, # toy
    'P': 0, # pee
    'R': 2, # read
    'S': 0, # sea
    'SH': 0, # she
    'T': 0, # tea
    'TH': 0, # theta
    'UH': 4, # hood
    'UW': 4, # two
    'V': 7, # vee
    'W': 7, # we
    'Y': 0, # yield
    'Z': 0, # zee
    'ZH': 0, # seizure
}

def get_phonemes(sentence: str) -> list:
    """
    Returns the phonetic representation of a sentence
    """

    def get_phonemes_single_word(word: str) -> list:
                # Check if the word is in the CMU Pronouncing Dictionary
        if word.lower() in prondict:
            # Get the phonetic representation (list of phonemes)
            phonemes = prondict[word.lower()][0]
        else:
            # If the word is not in the dictionary, return each letter
            phonemes = [prondict[letter][0][0] for letter in word.lower()]
        return phonemes

    return [get_phonemes_single_word(word) for word in nltk.word_tokenize(sentence)]
