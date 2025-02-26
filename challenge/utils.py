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
