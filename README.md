# LLM Crossword Solver Challenge

## Overview
Welcome to the AI Engineer technical challenge for i.AI 👩‍💻

The Prime Minister has an urgent request! Due to the high workload of the job, they need help solving their essential morning crossword. In this exercise, you'll build a LLM powered crossword puzzle solver that demonstrates your software engineering and AI skills.

## Challenge Structure
This interview will be split into 2 sections:
- **Part 1**: 1 hour private coding time
- **Part 2**: 45 minutes paired programming session

After working on the individual coding task, you will pair program with an interviewer to discuss your solution and continue developing the crossword puzzle solver.

When the interview is over please send a zip file of your code to the interviewer.

## Guidelines
* Try to build an efficient and fast solution
* Focus on clean, maintainable code
* Be prepared to talk about key decisions and tradeoffs
* There is no single correct solution that we are looking for
* You are not expected to complete the entire challenge, but you should be able to explain how you could get there

## Tasks

### Part 1: Individual Coding Task 
* **Time**: 60 minutes
* **AI assisted coding**: Allowed ✅ 

#### Tasks 
##### Task 1. Build an LLM powered crossword puzzle solver for `data/easy.puz`

The solver should:
1. Read the clues and provide possible answers
2. Resolve any conflicting answers
3. Return a completed crossword as a result

#### Task 2. Try to extend your solution to work for the other crosswords
* The medium puzzle in `data/medium.puz`
* The hard puzzle in `data/hard.puz`
* The cryptic puzzle in `data/cryptic.puz`

We provide a `main.py` script to help you get started. However, you can structure your code whichever way you think is best. We also provide a `scratchpad.ipynb` notebook to help you experiment with trying different solutions.

The crossword answers are included with the puzzles to help you validate your solutions, but your solution should complete the crossword without seeing any answers.

> **Note**: You can use any libraries or tools to build your solution. We also provide an OpenAI API if you prefer to use that.


### Part 2: Paired Programming 
* **Time**: 45 minutes
* **AI assisted coding**: Allowed ✅

#### Tasks 
1. Discuss and work with the interviewers to improve your solution to part 1
2. Implement the missing unit tests for the crossword class

## Setup Instructions

1. Clone this repository:
```bash
git clone <repo>
cd llm-crossword
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
cp .env.example .env #Copy the example env
# Edit the .env with and replace with the values provided during the interview
```

5. Verify setup:

Run the main script:
```bash
python main.py
```

Or run the notebook cells in scratchpad.ipynb:

6. Start coding!

## Project Structure

```
llm_crossword/
├── src/                 # Source code
├── tests/              # Test suite
└── data/               # Data files
```

## Testing

Run the test suite:
```bash
pytest
```

## License

This challenge is proprietary and confidential. Do not share or distribute.
