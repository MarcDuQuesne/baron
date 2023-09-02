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
    'AE': 0, # at
    'AH': 0, # hut
    'AO': 0, # ought
    'AW': 0, # cow
    'AY': 0, # hide
    'B': 0, # be
    'CH': 0, # cheese
    'D': 0, # dee
    'DH': 0, # thee
    'EH': 0, # Ed
    'ER': 0, # hurt
    'EY': 0, # ate
    'F': 0, # fee
    'G': 0, # green
    'HH': 0, # he
    'IH': 0, # it
    'IY': 0, # eat
    'JH': 0, # gee
    'K': 0, # key
    'L': 0, # lee
    'M': 0, # me
    'N': 0, # knee
    'NG': 0, # ping
    'OW': 0, # oat
    'OY': 0, # toy
    'P': 0, # pee
    'R': 0, # read
    'S': 0, # sea
    'SH': 0, # she
    'T': 0, # tea
    'TH': 0, # theta
    'UH': 0, # hood
    'UW': 0, # two
    'V': 0, # vee
    'W': 0, # we
    'Y': 0, # yield
    'Z': 0, # zee
    'ZH': 0, # seizure
}

def get_phonemes(word: str) -> list:
    """
    Returns the phonetic representation of a word
    """
    # Check if the word is in the CMU Pronouncing Dictionary
    if word.lower() in prondict:
        # Get the phonetic representation (list of phonemes)
        phonemes = prondict[word.lower()][0]
    else:
        # If the word is not in the dictionary, return each letter
        phonemes = [prondict[letter][0][0] for letter in word.lower()]
    return phonemes


if __name__ == "__main__":
    # Example sentence
    sentence = "Some and sum produce similar sounds."

    # Tokenize the sentence
    words = nltk.word_tokenize(sentence)

    # Extract phonetic representations and their lengths for each word
    for word in words:
        phonemes, length = get_phonemes(word)
        print(f"Word: {word}, Phonetic Representation: {phonemes}, Length: {length}")
