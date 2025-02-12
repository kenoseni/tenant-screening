from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch
from challenge.screening_processor import ScreeningProcessor

tenant = Tenant("John", "Doe", "1990-01-01", "USA", ["12345"])
blacklist = [
    BlacklistMatch("John", "Doe", "1990-01-01", "USA", "ProviderX", 90),
    BlacklistMatch("Johnny", "Doe", "", "Canada", "ProviderY", 50),
    BlacklistMatch("Jane", "Smith", "1985-02-02", "UK", "ProviderY", 80),
]

if __name__ == "__main__":
    screening_processor = ScreeningProcessor(tenant, blacklist, allowed_blacklist_sources=["ProviderX", "ProviderY"])
    screening_processor.classify_matches()