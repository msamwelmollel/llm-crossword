import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
from src.crossword.utils import load_puzzle

# Load environment variables from .env file
load_dotenv()

# Load the puzzle
puzzle = load_puzzle("data/medium.puz")


def extract_word_from_response(response_text, length):
    """
    Extract a word of the given length from the API response.
    """
    # Normalize the response by removing punctuation and extra spaces
    cleaned_response = re.sub(r'[^\w\s]', '', response_text).strip()
    print(f"Cleaned response: {cleaned_response}")
    
    # Use regex to extract a word of the required length
    match = re.search(rf'\b[a-zA-Z]{{{length}}}\b', cleaned_response)
    if match:
        return match.group(0).upper()  # Return the word in uppercase
    else:
        raise ValueError(f"Could not find a {length}-letter word in response: {response_text}")

        
def validate_word_placement(clue, word):
    if len(word) != clue.length:
        raise ValueError(f"Word length mismatch: Expected {clue.length}, got {len(word)}.")
    # Additional validation can include checking grid boundaries, overlapping words, etc.


def get_answer_to_clue(clue):
    client = AzureOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that solves crossword clues."},
                {"role": "user", "content": f"Provide a {clue.length}-letter word that fits the clue: '{clue.text}'. Only return the word, nothing else."}
            ],
            max_tokens=100,
            temperature=0.1
        )
        raw_response = response.choices[0].message.content.strip()
        print(f"Raw API response: {raw_response}")
        
        # Extract the word
        word = extract_word_from_response(raw_response, clue.length)
        print(f"Extracted word: {word}")
        
        # Validate word length
        validate_word_placement(clue, word)
        
        # Return as a list of characters
        return list(word)
    except Exception as e:
        print(f"Error getting answer for clue: {e}")
        return None


print('--- Solving the Puzzle ---')
for clue in puzzle.clues:
    print(f"Solving clue: {clue}")
    answer_chars = get_answer_to_clue(clue)
    if answer_chars:
        try:
            puzzle.set_clue_chars(clue, answer_chars)
        except Exception as e:
            print(f"Error setting clue chars: {e}")

print('--- Completed All? ---')
print(puzzle.validate_all())
print(puzzle)


# print('--- Solving the Puzzle ---')
# for clue in puzzle.clues:
#     print(f"Solving clue: {clue}")
#     answer_chars = get_answer_to_clue(clue)
#     if answer_chars:
#         try:
#             puzzle.set_clue_chars(clue, answer_chars)
#         except Exception as e:
#             print(f"Error setting clue chars: {e}")

# print('--- Completed All? ---')
# print(puzzle.validate_all())
# print(puzzle)