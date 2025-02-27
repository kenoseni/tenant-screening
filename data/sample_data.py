from challenge.tenant import Tenant

# Example tenants
tenants = [
    Tenant("John", "Doe", "1990-01-01", "USA", ["12345"]),
    Tenant("Jane", "Smith", "1985-02-02", "UK", ["67890"]),
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
                        "identificationNumber": ["12345"],
                    }
                ],
            }
        },
    }
]
