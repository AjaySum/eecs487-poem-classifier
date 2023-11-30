import string
import nltk
from rhymetagger import RhymeTagger
import re
import pronouncing
from string import punctuation
import numpy as np
# nltk.download('cmudict')  # Download the CMU Pronouncing Dictionary

d = nltk.corpus.cmudict.dict()

def count_syllables(word): 
    """Count number of syllables in a word."""
    # word = ''.join(char for char in word if char not in string.punctuation)
    # word = word.lower()

    # print("PROCESSED: ", word)
    
    if word in d:
        syllable_count = max([len(list(y for y in x if y[-1].isdigit())) for x in d[word]])
        #   print(f"The number of syllables in '{word}' is: {syllable_count}")
        return syllable_count
    else:
        # If the word is not found in the dictionary, a simple fallback method
        # could be implemented, for example, by counting the number of vowels.
        # vowels = "aeiouy"
        # return sum(1 for char in word if char in vowels)
    
        vowels = "aeiouy"
        count = 0
        prev_char_was_vowel = False

        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    count += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False

        # Adjust for silent 'e' at the end
        if word.lower().endswith('e') and count > 1:
            count -= 1

        print(f"BACKUPPPPPPPPPP The number of syllables in '{word}' is: {count}")      
        return count


def word_rhyme(poem):
    """"Detects if the words rhyme"""""
    print(poem)
    rt = RhymeTagger()
    rt.load_model(model = 'en')
    rhymes = rt.tag(poem, output_format=3) 
    print(rhymes)
    return rhymes
    # rt2 = RhymeTagger.new_model(lang = "en")
    # rt2.add_to_model()

def get_syllabic_stress(word):
    syllables = d.get(word.lower(), [])
   # print(syllables)
    if syllables:
        return [1 if any(char.isdigit() for char in s) else 0 for s in syllables[0]]
    else:
        # Handle unknown words
        return []
    
def scan_line(line):
    stress_pattern = [get_syllabic_stress(word) for word in line]
    #print(stress_pattern)
    scansion = ['/' if sum(pattern) == 1 else 'x' for pattern in stress_pattern]
    return ''.join(scansion)

def get_syllables(word):
    """
    Look up a word in the CMU dictionary, return a list of syllables
    """

    try:
        return d[word.lower()]
    except KeyError:
        return False


def stress(word):
    """
    Represent strong and weak stress of a word with a series of 1's and 0's
    """

    syllables = get_syllables(word)

    if syllables:
        # TODO: Implement a more advanced way of handling multiple pronunciations than just picking the first
        pronunciation_string = ''.join(syllables[0])
        # Not interested in secondary stress
        stress_numbers = ''.join([x.replace('2', '1')
                                  for x in pronunciation_string if x.isdigit()])

        return stress_numbers

    # Provisional logic for adding stress when the word is not in the dictionary is to stress first syllable only
    return '1' + '0' * (count_syllables(word) - 1)
    

    

