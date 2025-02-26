from challenge.screening_processor import ScreeningProcessor
from challenge.generate_test_data import tenants
from challenge.generate_test_data import blacklist

print("Input for Prospective Tenants:", tenants)

print("Search Result from Third-Party:", blacklist)


if __name__ == "__main__":
    for tenant in tenants:
        screening_processor = ScreeningProcessor(
            tenant,
            blacklist,
            allowed_blacklist_sources=[
                "Provider1-blacklist",
                "Provider2-blacklist",
                "Provider3-blacklist",
                "Provider4-blacklist",
                "Provider5-blacklist",
                "refinitiv-blacklist"

            ],
        )
        # Pass False to use manual algorithm
        screening_processor.classify_matches()
