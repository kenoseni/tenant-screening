import pytest
from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch
from challenge.screening_processor import ScreeningProcessor


@pytest.fixture
def sample_tenant():
    from challenge.tenant import Tenant

    return Tenant("John", "Doe", "1990-01-01", "USA", ["12345"])


@pytest.fixture
def sample_pipeline():
    return [
        {
            "type": "providerX-blacklist",
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
                            "exclusionMatchScore": 90.0,
                            "identificationNumber": ["12345"],
                        },
                        {
                            "name": "Jane",
                            "surname": "Smith",
                            "birthDate": "1985-02-02",
                            "birthCountry": "UK",
                            "providerId": "ProviderX",
                            "exclusionMatchScore": 80.0,
                            "identificationNumber": ["22395"],
                        },
                    ],
                }
            },
        },
        {
            "type": "providerY-blacklist",
            "result": {
                "data": {
                    "found": True,
                    "matches": [
                        {
                            "name": "Johnny",
                            "surname": "Doe",
                            "birthDate": "",
                            "birthCountry": "Canada",
                            "providerId": "ProviderY",
                            "exclusionMatchScore": 50.0,
                            "identificationNumber": ["12345"],
                        },
                    ],
                }
            },
        },
    ]


@pytest.fixture
def sample_blacklist(sample_pipeline):
    return ScreeningProcessor.extract_blacklist_matches(sample_pipeline)


@pytest.fixture
def screening_processor(sample_tenant, sample_blacklist):
    return ScreeningProcessor(
        sample_tenant,
        sample_blacklist,
        allowed_blacklist_sources=["ProviderX_blacklist", "ProviderY_blacklist"],
    )
