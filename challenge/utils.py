import random
import string
from challenge.tenant import Tenant


def clean_string(value):
    return value.strip().lower() if value else ""

# Function to generate random names
def random_name():
    return ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10)))

# Function to generate random dates
def random_date():
    return f"{random.randint(1950, 2020)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}"

def random_id():
    return ''.join(random.choices(string.digits, k=6))


# Generate 50 random tenants
tenants = [
    Tenant(
        first_name=random_name(),
        last_name=random_name(),
        birth_date=random.choice([random_date(), None]),
        nationality=random.choice(["USA", "UK", "Canada", "Germany", "MEX", None]),
        id_numbers=[random_id() for _ in range(random.randint(0, 3))]
    )
    for _ in range(50)
]

pipeline = [
    {
        "type": f"provider{random.randint(1, 5)}_blacklist",
        "result": {
            "data": {
                "found": random.choice([True, False]),
                "matches": [
                    {
                        "name": random.choice([t.first_name, random_name()]),
                        "surname": random.choice([t.last_name, random_name()]),
                        "birthDate": random.choice([t.birth_date, random_date(), None]),
                        "birthCountry": random.choice([t.nationality, "Unknown"]),
                        "providerId": f"Provider{random.randint(1, 5)}",
                        "exclusionMatchScore": random.randint(30, 100),
                    }
                ] if random.choice([True, False]) else []
            }
        }
    }
    for t in tenants
]
