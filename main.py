from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch
from challenge.screening_processor import ScreeningProcessor
from challenge.utils import tenants, blacklist

from pprint import pprint



pprint(tenants)

pprint(blacklist)



if __name__ == "__main__":
    for tenant in tenants:
        screening_processor = ScreeningProcessor(tenant, blacklist, allowed_blacklist_sources=["Provider1", "Provider2", "Provider3", "Provider4", "Provider5"])
        screening_processor.classify_matches()