from challenge.screening_processor import ScreeningProcessor
from challenge.utils import tenants, blacklist

print("Input for Prospective Tenants:", tenants)

print("Search Result from Third-Party:", blacklist)



if __name__ == "__main__":
    for tenant in tenants:
        screening_processor = ScreeningProcessor(tenant, blacklist, allowed_blacklist_sources=["Provider1", "Provider2", "Provider3", "Provider4", "Provider5"])
        # Pass False to use manual algorithm
        screening_processor.classify_matches(True)