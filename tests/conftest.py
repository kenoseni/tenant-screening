import pytest
from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch
from challenge.screening_processor import ScreeningProcessor


@pytest.fixture
def sample_tenant():
    from challenge.tenant import Tenant

    return Tenant("John", "Doe", "1990-01-01", "USA", ["12345"])


@pytest.fixture
def sample_blacklist():
    from challenge.black_list_match import BlacklistMatch

    return [
        BlacklistMatch("John", "Doe", "1990-01-01", "USA", "ProviderX", 90, ["12345"]),
        BlacklistMatch("Johnny", "Doe", "", "Canada", "ProviderY", 50, ["12345"]),
        BlacklistMatch("Jane", "Smith", "1985-02-02", "UK", "ProviderY", 80, ["22395"]),
    ]


@pytest.fixture
def screening_processor(sample_tenant, sample_blacklist):
    return ScreeningProcessor(
        sample_tenant,
        sample_blacklist,
        allowed_blacklist_sources=["ProviderX", "ProviderY"],
    )
