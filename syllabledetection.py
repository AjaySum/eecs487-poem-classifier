import string
import nltk
nltk.download('cmudict')  # Download the CMU Pronouncing Dictionary

# Count number of syllables in a word
def count_syllables(word):
    # print('00000')
    d = nltk.corpus.cmudict.dict()
    # print("11111")
    # print(type(d.keys()))
    word = ''.join(char for char in word if char not in string.punctuation)
    word = word.lower()
    # print('22222')
    # if d.keys().find(word):
    if word in d:
        syllable_count = max([len(list(y for y in x if y[-1].isdigit())) for x in d[word]])
        print(f"The number of syllables in '{word}' is: {syllable_count}")
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

# # Example usage:
# word = "example"
# syllable_count = count_syllables(word)
# print(f"The number of syllables in '{word}' is: {syllable_count}")

