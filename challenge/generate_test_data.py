import random
from challenge.tenant import Tenant
from challenge.utils import random_name, random_date, random_id
from challenge.screening_processor import ScreeningProcessor

# Generate 3 or more random tenants
tenants = [
    Tenant(
        first_name=random_name(),
        last_name=random_name(),
        birth_date=random.choice([random_date(), None]),
        nationality=random.choice(["USA", "UK", "Canada", "Germany", "MEX", None]),
        id_numbers=[random_id() for _ in range(random.randint(0, 3))],
    )
    for _ in range(3)
]


def generate_pipeline():
    """Generates a sample pipeline for tenant screening.

    IT SHOULD BE MODIFIED FOR THE ACTUAL PIPELINE DATA
    """

    pipeline = [
        {
            "type": f"provider{random.randint(1, 5)}_blacklist",
            "result": {
                "data": {
                    "found": random.choice([True, True]),
                    "matches": (
                        [
                            {
                                "name": random.choice([t.first_name, random_name()]),
                                "surname": random.choice([t.last_name, random_name()]),
                                "birthDate": random.choice(
                                    [t.birth_date, random_date(), None]
                                ),
                                "birthCountry": random.choice(
                                    [t.nationality, "Unknown"]
                                ),
                                "providerId": f"Provider{random.randint(1, 5)}-blacklist",
                                "exclusionMatchScore": random.randint(30.0, 100.0),
                                "identificationNumber": random.choice(
                                    [
                                        t.id_numbers,
                                        [
                                            random_id()
                                            for _ in range(random.randint(0, 3))
                                        ],
                                    ]
                                ),
                            }
                            for _ in range(random.randint(0, 3))
                        ]
                        if random.choice([True, True])
                        else []
                    ),
                }
            },
        }
        for t in tenants
    ]

    return pipeline


pipeline = generate_pipeline()

blacklist = ScreeningProcessor.extract_blacklist_matches(pipeline)
