import random
import string
from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch


def clean_string(value):
    return value.strip().lower() if value else ""


# Function to generate random names
def random_name():
    return "".join(random.choices(string.ascii_letters, k=random.randint(3, 10)))


# Function to generate random dates
def random_date():
    return f"{random.randint(1950, 2020)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}"


def random_id():
    return "".join(random.choices(string.digits, k=6))


def print_tenants(tenants):
    print("=====================================")
    print("Prospective Tenants:")
    print("=====================================")
    for i, tenant in enumerate(tenants, 1):
        tenant_str = (
            f"first_name={tenant.first_name}, last_name={tenant.last_name}, "
            f"birth_date={tenant.birth_date}, nationality={tenant.nationality}, "
            f"id_numbers={tenant.id_numbers}"
        )
        print(f"- Tenant {i}: {tenant_str}")


def print_blacklist_entries(blacklist):
    print("=====================================")
    print("Blacklist Entries Generated from Pipeline:")
    print("=====================================")
    for i, entry in enumerate(blacklist, 1):
        entry_str = (
            f"name={entry.name}, surname={entry.surname}, birth_date={entry.birth_date}, "
            f"birth_country={entry.birth_country}, provider={entry.provider}, "
            f"exclusion_score={entry.exclusion_score}, "
            f"identification_number={entry.identification_number}"
        )
        print(f"- Entry {i}: {entry_str}")


def print_screening_results(tenant: Tenant, results):
    print(
        f"================================================================================================================================================"
    )
    print(
        f"Screening Results for Tenant first_name: {tenant.first_name} last_name: {tenant.last_name} dob: {tenant.birth_date} id_numbers: {tenant.id_numbers} birth_country: {tenant.nationality}:"
    )
    print(
        f"=================================================================================================================================================="
    )
    for result in results:
        result_str = (
            f"Name: {result['name']}, Surname: {result['surname']}, DoB: {result['date_of_birth']}, ID_Numbers: {result['identification_number']}, Birth_Country: {result['birth_country']}, "
            f"Match Score: {result['match_score']}, Classification: {result['classification']}"
        )
        print(f"- {result_str}")


def print_pipeline_results(pipeline):
    """
    Prints the pipeline results in a readable format.

    Args:
        pipeline (list): A list of dictionaries, where each dictionary contains
                         'type' (str) and 'result' (dict with nested data including 'matches').
    """
    print("=====================================")
    print("Pipeline Results:")
    print("=====================================")
    for i, step in enumerate(pipeline, 1):
        # Extract the step type, defaulting to 'Unknown' if not present
        step_type = step.get("type", "Unknown")

        # Extract the matches from the result, navigating the nested structure
        # Default to an empty list if the path is missing
        matches = step.get("result", {}).get("data", {}).get("matches", [])
        num_matches = len(matches)

        # Print the step details
        print(f"- Step {i}: Type={step_type}, Matches Found={num_matches}")
