from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch

def ai_prompt(tenant: Tenant, blacklist_entry: BlacklistMatch):
    """Returns the prompt for a given tenant and blacklist entry"""

    prompt = f"""
        You are an AI assistant specialized in prospective tenant screening trained to assess blacklist matches.
        Your task is to analyze the provided tenant details against a blacklist match and classify the match strictly.
        if the Exclusion Score is greater or equal to 85, and name similarity is very high add 30 to the overall score
        if the Exclusion Score is greater or equal to 70, and name similarity is very high add 15 to the overall score

        ## Tenant Information:
        - First Name: {tenant.first_name}
        - Last Name: {tenant.last_name}
        - Birth Date: {tenant.birth_date}
        - Nationality: {tenant.nationality}
        - ID Numbers: {tenant.id_numbers}

        ## Blacklist Match Information:
        - Name: {blacklist_entry.name}
        - Surname: {blacklist_entry.surname}
        - Birth Date: {blacklist_entry.birth_date}
        - Birth Country: {blacklist_entry.birth_country}
        - Provider: {blacklist_entry.provider}
        - Exclusion Score: {blacklist_entry.exclusion_score}

        ## Evaluation Criteria:
        - Name Similarity
        - Birth Date Match
        - Nationality/Birth Country Match
        - Exclusion Score

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
        """
    return prompt
