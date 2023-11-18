import sys
from syllabledetection import count_syllables

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            content = content.split()
            for word in content:
                # print(content[6])
                count_syllables(word)
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

    # Read the content of the specified file
    text_content = read_text_file(file_path)

    if text_content is not None:
        print("File content:")
        print(text_content)
