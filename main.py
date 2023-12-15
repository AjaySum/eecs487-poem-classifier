import sys
import utils
import poemDetector
import string
import pronouncing
from datasets import load_dataset
haikus = load_dataset("statworx/haiku")
from PoemSentimentDetector import PoemSentimentDetector
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
def read_text_file(file_path):
    """Read poem from inputted text file."""
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
            content = file.read()
            content = content.split('\n')
            punctuation_string = string.punctuation + "…"

            for i in range(len(content)):
               
                clean_content = ''
                for char in content[i]:
                    if char == '’' or char == "'":
                        clean_content += "'"
                    elif char not in punctuation_string:
                        clean_content += char
                   
                content[i] = clean_content.lower()
               
            print("CLEANED POEM: ", content)
            poemDetector.detectHaiku(content)
            poemDetector.detectLimerick(content)
            poemDetector.detectBallad(content)
            poemDetector.detectSonnet(content)
            poemDetector.detectVillanelle(content)
            poemDetector.detectBlankVerse(content)
            poemDetector.detectFreeVerse(content)

            return content
        
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# def evaluate_poem_type(elegy_detector, poem_type, folder_path):
#     poem_data = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(folder_path, filename)
#             poem_content = read_text_file(file_path)
#             if poem_content is not None:
#                 result = elegy_detector.predict(poem_content)
#                 poem_data.append((result[0], poem_type))

    
#     true_labels = [poem[1] for poem in poem_data]
    
    
#     predicted_labels = [poem[0] for poem in poem_data]

#     accuracy = accuracy_score(true_labels, predicted_labels)
#     f1 = f1_score(true_labels, predicted_labels, pos_label=poem_type)
#     precision = precision_score(true_labels, predicted_labels, pos_label=poem_type)
#     recall = recall_score(true_labels, predicted_labels, pos_label=poem_type)

#     print(f"Metrics for {poem_type}:")
#     print(f"Accuracy: {accuracy}")
#     print(f"F1-Score: {f1}")
#     print(f"Precision: {precision}")
#     print(f"Recall: {recall}")
   

if __name__ == "__main__":
    # Check if the user provided a file path as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Sample themes for both elegy and ode
    elegy_themes = [
        "mourning",
        "loss",
        "grief",
        "death",
        "memories",
        "reflection",
        "transience",
        "solitude"
    ]
    ode_themes = [
        "celebration",
        "praise",
        "beauty",
        "inspiration",
        "awe",
        "gratitude",
        "nature",
        "love"
    ]

    # train sentiment detector
    sentiment_detector = PoemSentimentDetector(elegy_themes, ode_themes)

    elegy_data, elegy_labels = sentiment_detector.load_data('data/poems/elegy')
    ode_data, ode_labels = sentiment_detector.load_data('data/poems/ode')

    all_data = elegy_data + ode_data
    all_labels = elegy_labels + ode_labels

    sentiment_detector.train(all_data, all_labels)

    poem_content = read_text_file(file_path)

    
    if poem_content is not None:
        result = sentiment_detector.predict(poem_content)
        print('This poem is:', result)
    else:
        print("Poem content is None. Cannot predict.")
