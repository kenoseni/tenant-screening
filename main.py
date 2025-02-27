from challenge.screening_processor import ScreeningProcessor

from challenge.utils import print_tenants, print_pipeline_results

from data.sample_data import tenants, pipeline

from challenge.constants import allowed_blacklist_sources

"""
Uncomment the import below if you want to test with more random data.
Note that `from data.sample_data import tenants, pipeline` should be commented out.
"""
# from challenge.generate_test_data import tenants, pipeline

print_tenants(tenants)

print_pipeline_results(pipeline)


if __name__ == "__main__":
    for tenant in tenants:
        """A filter_type can be passed as the 4th argument to the .from_pipeline method

        screening_processor = ScreeningProcessor.from_pipeline(
            tenant, pipeline, allowed_blacklist_sources=allowed_blacklist_sources, "refinitiv-blacklist"
        )

        if filter_type is not passed "refinitiv-blacklist" is used by default
        """
        screening_processor = ScreeningProcessor.from_pipeline(
            tenant, pipeline, allowed_blacklist_sources=allowed_blacklist_sources
        )
        # Pass False to use manual algorithm
        screening_processor.classify_matches()
