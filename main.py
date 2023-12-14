import sys
import utils
import poemDetector
import string
import pronouncing
from datasets import load_dataset
haikus = load_dataset("statworx/haiku")
import elegydetector
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
            content = file.read()
            content = content.split('\n')
            # # punctuation_string = string.punctuation + '’'
            punctuation_string = string.punctuation + "…"

            for i in range(len(content)):
                # sent_syllables = 0
                clean_content = ''
                for char in content[i]:
                    if char == '’' or char == "'":
                        clean_content += "'"
                    elif char not in punctuation_string:
                        clean_content += char
                    #content[i] = ''.join(char for char in content[i] if char not in punctuation_string)
                # content[i] = content[i].lower()
                content[i] = clean_content.lower()
                # for word in sent.split():
                #     sent_syllables += utils.count_syllables(word)
                # print(f"{sent}: {sent_syllables}")
            print("CLEANED POEM: ", content)
            poemDetector.detectHaiku(content)
            poemDetector.detectLimerick(content)
            poemDetector.detectBallad(content)
            poemDetector.detectSonnet(content)
            poemDetector.detectVillanelle(content)
            poemDetector.detectBlankVerse(content)
            poemDetector.detectFreeVerse(content)

            # for line in content:
            # print(utils.meter_detector(content))

            # poem = [''.join(word for word in content)]
            # poem = ["I like pie", 
            # "pie says hi"]
            # poem = ["unchangeable", "swell"]
            # word_rhyme(poem)
            #           # print(poem)
            # utils.word_rhyme(content)

            # word = "shall"
            # word2 = "i"
            # val = utils.stress(word)
            # val2 = utils.stress(word2)
            # print(val)     
            # print(val2)   
            # sent2 = "i love poetry"
            #val4 = utils.get_line_scansion(sent2)
            #print(val4)



            # sent1 = ["shall", "i", "compare", "thee", "to", "a", "summer's", "day"]
            # # sent1 = "re.compile(r'((\b\w*-*\w*\b)\s?){5}$')"
            # for word in sent1:
            #     print(utils.stress(sent1))
            # # val3 = utils.detect_iambic_pentameter(sent1)
            # # print(val3)

            sent1 = ["shall", "i", "compare", "thee", "to", "a", "summer's", "day"]

            return content
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Check if the user provided a file path as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python read_file.py <file_path>")
        sys.exit(1)

    # Get the file path from the command-line argument
    file_path = sys.argv[1]

    ed = elegydetector.ElegyDetector()

    elegy_data = ed.load_data('elegy')
    
    
    other_poem_data = []
    poem_types = ['sonnet', 'ballad', 'ode', 'villanelle']  # add more (find way to do all fast)
    for poem_type in poem_types:
        data = ed.load_data(f'data/poems/{poem_type}')
        other_poem_data.extend(data)


    ed.train(elegy_data, other_poem_data)
    poem_content = read_text_file(file_path)
    result = ed.predict(poem_content)
    print('This poem is:', result[0])