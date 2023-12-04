import sys
import utils
import poemDetector
import string
import pronouncing
import elegydetector
import os
# from datasets import load_dataset
# haikus = load_dataset("statworx/haiku")

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# def run_program():
#         poem = ["I like pie", 
#             "pie says hi"]
#         # print(poem)
#         word_rhyme(poem)

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