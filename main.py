from challenge.screening_processor import ScreeningProcessor
from challenge.generate_test_data import tenants, pipeline
from challenge.utils import print_tenants, print_pipeline_results

print_tenants(tenants)

print_pipeline_results(pipeline)


if __name__ == "__main__":
    for tenant in tenants:
        screening_processor = ScreeningProcessor.from_pipeline(
            tenant,
            pipeline,
            allowed_blacklist_sources=[
                "Provider1-blacklist",
                "Provider2-blacklist",
                "Provider3-blacklist",
                "Provider4-blacklist",
                "Provider5-blacklist",
                "refinitiv-blacklist",
            ],
        )
        # Pass False to use manual algorithm
        screening_processor.classify_matches()
