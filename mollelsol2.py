# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 13:19:16 2024

@author: msamwelmollel
"""

import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
from src.crossword.utils import load_puzzle

load_dotenv()
puzzle = load_puzzle("data/easy.puz")

def extract_word_from_response(response_text, length):
    # Look for a word in quotes or after "is" or at the end of the response
    patterns = [
        rf"['\"](.*?)['\"]",  # Words in quotes
        rf"is ['\"]*([A-Za-z]{{{length}}})['\"]*",  # Words after "is"
        rf"is ['\"]*([A-Za-z]{{{length}}})['\"]*\.",  # Words ending with period
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        for match in matches:
            word = match.strip(' ."\'')
            if len(word) == length and word.isalpha():
                return word.upper()
    
    # Fallback: look for any word of the correct length
    words = re.findall(r'\b[A-Za-z]+\b', response_text)
    for word in words:
        if len(word) == length and word.isalpha():
            return word.upper()
            
    raise ValueError(f"Could not find a {length}-letter word in response: {response_text}")

def validate_word_placement(clue, word):
    if len(word) != clue.length:
        raise ValueError(f"Word length mismatch: Expected {clue.length}, got {len(word)}.")

def get_answer_to_clue(clue):
    client = AzureOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    try:
        # Using deployment name from environment variable
        deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a crossword puzzle solver. Provide only the answer word, with no additional explanation."},
                {"role": "user", "content": f"Give the {clue.length}-letter answer for this crossword clue: '{clue.text}'"}
            ],
            max_tokens=50,
            temperature=0
        )
        raw_response = response.choices[0].message.content.strip()
        print(f"Raw API response: {raw_response}")
        
        word = extract_word_from_response(raw_response, clue.length)
        print(f"Extracted word: {word}")
        
        validate_word_placement(clue, word)
        return list(word)
    except Exception as e:
        print(f"Error getting answer for clue: {e}")
        return None

print('--- Solving the Puzzle ---')
for clue in puzzle.clues:
    print(f"\nSolving clue: {clue}")
    answer_chars = get_answer_to_clue(clue)
    if answer_chars:
        try:
            puzzle.set_clue_chars(clue, answer_chars)
            print(f"Set answer: {''.join(answer_chars)}")
        except Exception as e:
            print(f"Error setting clue chars: {e}")

print('\n--- Completed All? ---')
print(puzzle.validate_all())
print(puzzle)