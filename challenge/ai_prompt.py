from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch

# Constants
SCORE_THRESHOLD_RELEVANT = 85
SCORE_THRESHOLD_REVIEW = 65
SCORE_THRESHOLD_NAME_ONLY = 60


def ai_prompt(tenant: Tenant, blacklist_entry: BlacklistMatch):
    """Returns the prompt for a given tenant and blacklist entry"""

    prompt = f"""
        You are an AI assistant specialized in prospective tenant screening trained to assess blacklist matches comprehensively.
        Your task is to analyze the provided tenant details against a blacklist match, considering all evaluation criteria equally,
        with particular attention to strong identifiers like birth date and identification numbers. Classify the match strictly based on the combined evidence.
        
        **Important**: If only the names match or are very similar, the confidence score must not exceed {SCORE_THRESHOLD_NAME_ONLY}.
        A high score (e.g., {SCORE_THRESHOLD_RELEVANT} or above) requires matches across multiple criteria.

        ## Tenant Information:
        - **First Name**: {tenant.first_name}
        - **Last Name**: {tenant.last_name}
        - **Birth Date**: {tenant.birth_date}
        - **Nationality**: {tenant.nationality}
        - **ID Numbers**: {tenant.id_numbers}

        ## Blacklist Match Information:
        - **Name**: {blacklist_entry.name}
        - **Surname**: {blacklist_entry.surname}
        - **Birth Date**: {blacklist_entry.birth_date}
        - **Birth Country**: {blacklist_entry.birth_country}
        - **Provider**: {blacklist_entry.provider}
        - **Exclusion Score**: {blacklist_entry.exclusion_score}
        - **Identification Numbers**: {blacklist_entry.identification_number}

        ## Evaluation Criteria:
        - **Name Similarity**
        - **Birth Date Match**
        - **Nationality/Birth Country Match**
        - **Exclusion Score**
        - **Identification Numbers Match**

        ## Expected Output:
        Respond **only** with a valid JSON object, strictly formatted as follows:
        ```json
        {{
          "ai_model_confidence_score": <integer between 0 and 100>,
          "match_classification": "<one of: 'Relevant Match', 'Probably Not Relevant', 'Needs Review', 'Invalid Source'>",
          "explanation": "<brief reasoning for the classification>"
        }}
        ```
        Do not include any text before or after the JSON response.

        ## Classification Guidelines:
        **'Relevant Match'**: match_score >= {SCORE_THRESHOLD_RELEVANT}
        **'Needs Review'**: match_score >= {SCORE_THRESHOLD_REVIEW} and < {SCORE_THRESHOLD_RELEVANT}
        **'Probably Not Relevant'**: score < {SCORE_THRESHOLD_REVIEW}
        **'Invalid Source'**: if the provider is incorrect

        Ensure your explanation details which criteria matched or did not, providing a balanced assessment beyond just name similarity.
        """
    return prompt.strip()
