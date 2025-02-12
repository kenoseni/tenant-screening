# Prospective Tenant Screening Via AI or Manually Using Various Criteria

## Overview

This project is an AI-driven prospective tenant screening system that evaluates search results (blacklist matches) using predefined criteria. The AI model assesses similarities in names, birth dates, nationality, ID numbers and the Exclusion Score returned from the search to determine the relevance of a blacklist match.

## Architectural Diagram

[Architecture](https://drive.google.com/file/d/1Uo_ePM-tvR5duFRxKy_dzzu1Ny54HAnF/view?usp=sharing)

## Features

- **Prospective Tenant Screening**: Compares prospective tenant details with search result from third-party provider (blacklist entries).
- **AI-Generated Confidence Score**: This ranges from 0 to 100, indicating the certainty of a match.
- **Manual Confidence Score**: This ranges from 0 to 100, indicating the certainty of a match.
- **Match Classification**:
  - **Relevant Match**: Strong indications that the prospective tenant is blacklisted.
  - **Probably Not Relevant**: A mismatches that suggest a false positive.
  - **Needs Review**: Some uncertain cases that requires further human verification.
  - **Invalid Source**: Blacklist data is unreliable because it was not returned from a listed provider.
- **Detailed Explanation**: Justifies classification decisions. This only present when the classification AI generated

## Installation

Ensure you have Python installed (preferably Python 3.11+). Then, install the required dependencies:

create a virtual environment

```sh
python -m venv <environment_name>

```

activate the virtual environment

```sh
source <environment_name>/bin/activate

```

install the required dependencies

```sh
pip install -r requirements.txt

```

run all unit tests

```sh
pytest -v

```

## Test Coverage

view test coverage

``sh
open htmlcov/index.html

````

install `ollama` via the terminal
for Mac OS use Homebrew

```sh
brew install ollama

````

install a Large language model(LLM) e.g. `llama3.2` into your machine from [LLM's](https://ollama.com/)

```sh
ollama run llama3.2

```

confirm you have the LLM installed by running

```sh
ollama list

```

## Configuration

create a `.env` file using the `.env.sample`

## Manual Testing

The dataset can be manipulated to test various scenarios

```sh
python main.py

```

## Response

- **AI classification response**: If the AI is available and evaluates the result, the following response is generated on the console with an `explanation` attribute:

```json
[
  {
    "name": "John",
    "surname": "Doe",
    "match_score": 95,
    "classification": "Relevant Match",
    "explanation": "High Exclusion Score (90) matches exact details, and no significant discrepancies in other criteria"
  },
  {
    "name": "Johnny",
    "surname": "Doe",
    "match_score": 50,
    "classification": "Probably Not Relevant",
    "explanation": "Birth Date: No match, Exclusion Score: Low (50)"
  },
  {
    "name": "Jane",
    "surname": "Smith",
    "match_score": 15.0,
    "classification": "Probably Not Relevant"
  }
]
```

- **Manual classification response**: If the AI is not available for any reason the manual result processing kicks in and evaluates the result, the following response is generated on the console with no `explanation` attribute:

```json
[
  {
    "name": "Jane",
    "surname": "Smith",
    "match_score": 15.0,
    "classification": "Probably Not Relevant"
  },
  {
    "name": "Kimberly",
    "surname": "Jordan",
    "match_score": 95.0,
    "classification": "Relevant Match"
  }
]
```

## Further improvements

- **API Development**: Build a RESTful API to interact with the system.
- **Enhanced Manual Classification**: Improve logic for manual classification.
- **Database Integration**: Store historical screening results for future reference.
- **Performance Optimization**: Optimize response time when using AI models.
- **Web Interface**: Create a web-based UI for easier interaction.
