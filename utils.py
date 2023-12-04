import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
# from nltk.corpus import uni
from rhymetagger import RhymeTagger
import re
import pronouncing
from string import punctuation
import numpy as np
# nltk.download('cmudict')  # Download the CMU Pronouncing Dictionary

d = nltk.corpus.cmudict.dict()
# t = nltk.download('universal_tagset')

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

def get_scansion_line(line):
    tokens = line.split()
    pos_tags = pos_tag(tokens)
    print(tokens)
    print(pos_tags)

    keep_list = ['NN', 'NNP', 'NNPS', 'NNS', 'VB', 'VBG', 'VBN', 'VBP', 'VBZ']

    scansion = []
    for i in range(len(tokens)):
        s = ""
        if tokens[i] in d:
            phonemes = d[tokens[i]][0]
            for phoneme in phonemes:
                # print(phoneme[-1])
                if phoneme[-1] == '1' or phoneme[-1] == '2':
                    # print("HERE")
                    s += '1'
                elif phoneme[-1] == '0':
                    s += '0'
                
            if pos_tags[i][1] not in keep_list and len(s) == 1:
                s = '0'
        else:
            s = '1' + '0' * (count_syllables(tokens[i]) - 1)

        if len(s) > 1:
            for char in s:
                scansion.append(char)
            # print(s)
        else:
            scansion.append(s)
    print(scansion)

    return scansion

def scansion_diff(scansion, correct):
    diff = 0
    for i in range(len(scansion)):
        if scansion[i] != correct[i]:
            diff += 1
    return diff

def meter_detector(poem):
    meters = {
        'iambic trimeter': ['0', '1', '0', '1', '0', '1'],
        'iambic tetrameter': ['0', '1', '0', '1', '0', '1', '0', '1'],
        'iambic pentameter': ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
        # 'trochaic bimeter' : ['1', '0', '1', '0'],
        'trochaic tetrameter': ['1', '0', '1', '0', '1', '0', '1', '0'],
        'trochaic pentameter': ['1', '0', '1', '0', '1', '0', '1', '0', '1', '0']
    }
    scansions = []
    for line in poem:
        scansion = get_scansion_line(line)
        scansions.append(scansion)

    size = len(scansions[0])

    if size == 6:
        correct = meters['iambic trimeter']
        found = True
        for scansion in scansions:
            diff = scansion_diff(scansion, correct)
            if diff/size > 0.34:
                found = False
                break
        if found == True:
            print("Could be iambic trimeter")
            return 'iambic trimeter'
        # return found
    elif size == 8:
        correct = [("iambic tetrameter", meters['iambic tetrameter']),
                   ("trochaic tetrameter", meters['trochaic tetrameter'])]
        
        for c in correct:
            found = True
            for scansion in scansions:
                diff = scansion_diff(scansion, c[1])
                if diff/size > 0.34:
                    found = False
                    break
            if found == True:
                print("Could be", c[0])
                return c[0]
        # return found
    elif size == 10:
        correct = [("iambic pentameter", meters['iambic pentameter']),
                   ("trochaic pentameter",meters['trochaic pentameter'])]
        
        for c in correct:
            found = True
            for scansion in scansions:
                diff = scansion_diff(scansion, c[1])
                if diff/size > 0.34:
                    found = False
                    break
            if found == True:
                print("Could be", c[0])
                return c[0]
        # return found
    
    return ''