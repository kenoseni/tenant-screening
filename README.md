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

Ensure you have Python `3.11+` installed. Then, install the required dependencies:

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

```sh
open htmlcov/index.html

```

## Configuration

create a `.env` file using the `.env.sample`

## Model

To use CHAT-GPT, add your `api_key` and specify a model in your `.env` file

```sh
OPENAI_API_KEY=<ADD YOUR API KEY>
OPENAI_MODEL=gpt-4o-mini
```

To use other models install `ollama` via the terminal for example on Mac OS run

```sh
brew install ollama

```

install a Large language model(LLM) e.g. `llama3.2` into your machine from [LLM's](https://ollama.com/)

```sh
ollama run llama3.2

```

confirm you have the LLM installed by running

```sh
ollama list

```

## Manual Testing

1. **Prepare Input Data**: Use the sample below or modify tenants and pipeline in `generate_test_data.py`.
2. **Run the Screening**:

```sh
python main.py
```

3. **View Results**: Check the terminal for tenant details, pipeline results, and classifications.

**Note**: to test without using the LLM model(manual classification) pass False to the classify_matches method in `main.py`

```python
screening_processor.classify_matches(False)
```

## Sample Input Data

Try this example to test immediately:

```python
# Example tenants
tenants = [
    Tenant("John", "Doe", "1990-01-01", "USA", ["12345"]),
    Tenant("Jane", "Smith", "1985-02-02", "UK", ["67890"])
]

# Example pipeline
pipeline = [
    {
        "type": "refinitiv-blacklist",
        "result": {
            "data": {
                "found": True,
                "matches": [
                    {
                        "name": "John",
                        "surname": "Doe",
                        "birthDate": "1990-01-01",
                        "birthCountry": "USA",
                        "providerId": "ProviderX",
                        "exclusionMatchScore": 90,
                        "identificationNumber": ["12345"]
                    }
                ]
            }
        }
    }
]
```

## Generate Random Input Data For Testing

Any test data can be used to test this application. The `tenant` data and `pipeline` data in the `generate_test_data` file can can be substituted with any other test data

## Response

- **AI classification response**: If the AI is available and evaluates the result, the following response is generated on the console with an `explanation` attribute:

```sh
=====================================
Prospective Tenants:
=====================================
- Tenant 1: first_name=sWyUQC, last_name=DYLfYOx, birth_date=1970-09-26, nationality=UK, id_numbers=['668811']
- Tenant 2: first_name=pChDCt, last_name=grqesNg, birth_date=, nationality=Germany, id_numbers=['126489', '880870']
- Tenant 3: first_name=dshZGj, last_name=QTue, birth_date=, nationality=Germany, id_numbers=['725480', '216011']
=====================================
Pipeline Results:
=====================================
- Step 1: Type=provider1_blacklist, Matches Found=3
- Step 2: Type=provider3_blacklist, Matches Found=2
- Step 3: Type=provider5_blacklist, Matches Found=0
=====================================
Blacklist Entries Generated from Pipeline:
=====================================
- Entry 1: name=jsrVf, surname=DYLfYOx, birth_date=1970-09-26, birth_country=UK, provider=Provider5-blacklist, exclusion_score=30, identification_number=['659545']
- Entry 2: name=sWyUQC, surname=fOR, birth_date=1998-10-13, birth_country=Unknown, provider=Provider3-blacklist, exclusion_score=36, identification_number=['668811']
- Entry 3: name=sWyUQC, surname=NMs, birth_date=1977-09-21, birth_country=Unknown, provider=Provider2-blacklist, exclusion_score=75, identification_number=[]
- Entry 4: name=pChDCt, surname=grqesNg, birth_date=, birth_country=Germany, provider=Provider3-blacklist, exclusion_score=54, identification_number=['126489', '880870']
- Entry 5: name=NIdTDRlR, surname=cGDSFyhRJ, birth_date=, birth_country=Unknown, provider=Provider1-blacklist, exclusion_score=62, identification_number=['248270', '801149', '971972']
================================================================================================================================================
Screening Results for Tenant first_name: sWyUQC last_name: DYLfYOx dob: 1970-09-26 id_numbers: ['668811'] birth_country: UK:
==================================================================================================================================================
- Name: jsrVf, Surname: DYLfYOx, DoB: 1970-09-26, ID_Numbers: ['659545'], Birth_Country: UK, Match Score: 80, Classification: Relevant Match
- Name: sWyUQC, Surname: fOR, DoB: 1998-10-13, ID_Numbers: ['668811'], Birth_Country: Unknown, Match Score: 60, Classification: Probably Not Relevant
- Name: sWyUQC, Surname: NMs, DoB: 1977-09-21, ID_Numbers: [], Birth_Country: Unknown, Match Score: 75, Classification: Probably Not Relevant
- Name: pChDCt, Surname: grqesNg, DoB: , ID_Numbers: ['126489', '880870'], Birth_Country: Germany, Match Score: 67, Classification: Needs Review
- Name: NIdTDRlR, Surname: cGDSFyhRJ, DoB: , ID_Numbers: ['248270', '801149', '971972'], Birth_Country: Unknown, Match Score: 74, Classification: Needs Review
```

`OR`

```json
[
  {
    "name": "John",
    "surname": "Doe",
    "date_of_birth": "",
    "birth_country": "",
    "exclusion_score": "",
    "identification_number": "",
    "provider": "",
    "match_score": 95,
    "classification": "Relevant Match",
    "explanation": "High Exclusion Score (90) matches exact details, and no significant discrepancies in other criteria"
  },
  {
    "name": "Johnny",
    "surname": "Doe",
    "date_of_birth": "",
    "birth_country": "",
    "exclusion_score": "",
    "identification_number": "",
    "provider": "",
    "match_score": 50,
    "classification": "Probably Not Relevant",
    "explanation": "Birth Date: No match, Exclusion Score: Low (50)"
  },
  {
    "name": "Jane",
    "surname": "Smith",
    "date_of_birth": "",
    "birth_country": "",
    "exclusion_score": "",
    "identification_number": "",
    "provider": "",
    "match_score": 15.0,
    "classification": "Probably Not Relevant"
  }
]
```

the following responses can also be gotten if the provider does not match. This indicates that the results from this providers are not relevant

```json
[]
```

- **Manual classification response**: If the AI is not available for any reason the manual result processing kicks in and evaluates the result, the following response is generated on the console with no `explanation` attribute:

```sh
=====================================
Prospective Tenants:
=====================================
- Tenant 1: first_name=jRDsk, last_name=smfbdCDteo, birth_date=2010-10-06, nationality=USA, id_numbers=[]
- Tenant 2: first_name=gLtf, last_name=KGq, birth_date=, nationality=MEX, id_numbers=['209095', '032176', '801937']
- Tenant 3: first_name=spXoyLtR, last_name=JUzIrnCuIZ, birth_date=, nationality=MEX, id_numbers=[]
=====================================
Pipeline Results:
=====================================
- Step 1: Type=provider2_blacklist, Matches Found=3
- Step 2: Type=provider5_blacklist, Matches Found=2
- Step 3: Type=provider3_blacklist, Matches Found=3
=====================================
Blacklist Entries Generated from Pipeline:
=====================================
- Entry 1: name=KxBPWdJP, surname=JgHYz, birth_date=, birth_country=Unknown, provider=Provider1-blacklist, exclusion_score=74, identification_number=['837300']
- Entry 2: name=jRDsk, surname=smfbdCDteo, birth_date=, birth_country=USA, provider=Provider5-blacklist, exclusion_score=32, identification_number=[]
- Entry 3: name=gnvP, surname=oRe, birth_date=, birth_country=USA, provider=Provider3-blacklist, exclusion_score=54, identification_number=['517345']
- Entry 4: name=VjQPkqq, surname=SJYlCwj, birth_date=, birth_country=MEX, provider=Provider5-blacklist, exclusion_score=80, identification_number=['209095', '032176', '801937']
- Entry 5: name=gLtf, surname=gKVbA, birth_date=, birth_country=MEX, provider=Provider2-blacklist, exclusion_score=83, identification_number=['209095', '032176', '801937']
- Entry 6: name=zLsn, surname=VBGDtlWkF, birth_date=1959-06-03, birth_country=Unknown, provider=Provider2-blacklist, exclusion_score=71, identification_number=[]
- Entry 7: name=spXoyLtR, surname=zRlMQeB, birth_date=, birth_country=Unknown, provider=Provider1-blacklist, exclusion_score=63, identification_number=['871622']
- Entry 8: name=EmklhyM, surname=MtevoY, birth_date=, birth_country=Unknown, provider=Provider4-blacklist, exclusion_score=46, identification_number=[]
================================================================================================================================================
Screening Results for Tenant first_name: jRDsk last_name: smfbdCDteo dob: 2010-10-06 id_numbers: [] birth_country: USA:
==================================================================================================================================================
- Name: KxBPWdJP, Surname: JgHYz, DoB: , ID_Numbers: ['837300'], Birth_Country: Unknown, Match Score: 15.0, Classification: Probably Not Relevant
- Name: jRDsk, Surname: smfbdCDteo, DoB: , ID_Numbers: [], Birth_Country: USA, Match Score: 50.0, Classification: Probably Not Relevant
- Name: gnvP, Surname: oRe, DoB: , ID_Numbers: ['517345'], Birth_Country: USA, Match Score: 20.0, Classification: Probably Not Relevant
- Name: VjQPkqq, Surname: SJYlCwj, DoB: , ID_Numbers: ['209095', '032176', '801937'], Birth_Country: MEX, Match Score: 15.0, Classification: Probably Not Relevant
- Name: gLtf, Surname: gKVbA, DoB: , ID_Numbers: ['209095', '032176', '801937'], Birth_Country: MEX, Match Score: 15.0, Classification: Probably Not Relevant
- Name: zLsn, Surname: VBGDtlWkF, DoB: 1959-06-03, ID_Numbers: [], Birth_Country: Unknown, Match Score: 15.0, Classification: Probably Not Relevant
- Name: spXoyLtR, Surname: zRlMQeB, DoB: , ID_Numbers: ['871622'], Birth_Country: Unknown, Match Score: 0.0, Classification: Probably Not Relevant
- Name: EmklhyM, Surname: MtevoY, DoB: , ID_Numbers: [], Birth_Country: Unknown, Match Score: 0.0, Classification: Probably Not Relevant
```

`OR`

```json
[
  {
    "name": "Jane",
    "surname": "Smith",
    "date_of_birth": "",
    "birth_country": "",
    "exclusion_score": "",
    "identification_number": "",
    "provider": "",
    "match_score": 15.0,
    "classification": "Probably Not Relevant"
  },
  {
    "name": "Kimberly",
    "surname": "Jordan",
    "date_of_birth": "",
    "birth_country": "",
    "exclusion_score": "",
    "identification_number": "",
    "provider": "",
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
