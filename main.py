import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from src.crossword.utils import load_puzzle

# Load environment variables from .env file
load_dotenv()

# Load the puzzle
puzzle = load_puzzle("data/first.puz")

print('--- Clues ---')
clue = puzzle.clues[0]
print(clue)

print('--- Set a guess ---')
puzzle.set_clue_chars(puzzle.clues[0], ["a", "b", "c"])
print(puzzle)

print('--- Entry is correct? ---')
print(puzzle.validate_clue_chars(clue))

print('--- Undo ---')
puzzle.undo()
print(puzzle)

print('--- Reveal Clue ---')
puzzle.reveal_clue_answer(clue)
print(puzzle)

print('--- Entry is correct? ---')
print(puzzle.validate_clue_chars(clue))

print('--- Completed all? ---')
print(puzzle.validate_all())

print('--- Reveal All ---')
puzzle.reveal_all()
print(puzzle)

print('--- Completed all? ---')
print(puzzle.validate_all())

print('--- Reset ---')
puzzle.reset()
print(puzzle)

print('--- OpenAI Hello World ---')
def openai_hello_world():
    client = AzureOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                  {"role": "user", "content": "Hello!"}]
    )
    return response.choices[0].message.content

print(openai_hello_world())
