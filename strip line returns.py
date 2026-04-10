-import os
def split_string_by_n(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]
def remove_line_returns(file_path):
    """
    Removes all line returns from a text file.

    Args:
        file_path (str): The path to the text file.
    """
    
        # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
      content = file.read()
    hugeList=content.split(",")
# --- Example Usage ---
# Replace 'your_file.txt' with the path to your actual text file
# Be careful: this script modifies the original file in place.
if __name__ == "__main__":
    file_to_process = 'mes.txt'
    # Optional: Create a dummy file for testing purposes
    # with open(file_to_process, 'w') as f:
    #     f.write("Line 1\nLine 2\r\nLine 3")

    remove_line_returns(file_to_process)
