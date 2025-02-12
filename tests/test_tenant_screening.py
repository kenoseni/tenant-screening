from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch
from challenge.screening_processor import ScreeningProcessor


def test_tenant_initialization(sample_tenant):
    assert sample_tenant.first_name == "John"
    assert sample_tenant.last_name == "Doe"
    assert sample_tenant.birth_date == "1990-01-01"
    assert sample_tenant.nationality == "USA"
    assert sample_tenant.id_numbers == ["12345"]


def test_blacklist_match_initialization(sample_blacklist):
    blacklist_entry = sample_blacklist[0]
    assert blacklist_entry.name == "John"
    assert blacklist_entry.surname == "Doe"
    assert blacklist_entry.birth_date == "1990-01-01"
    assert blacklist_entry.provider == "ProviderX"
    assert blacklist_entry.exclusion_score == 90


def test_screening_processor_initialization(screening_processor, sample_tenant, sample_blacklist):
    assert screening_processor.tenant == sample_tenant
    assert screening_processor.blacklist_entries == sample_blacklist
    assert screening_processor.allowed_blacklist_sources == ["ProviderX", "ProviderY"]


def test_name_similarity(screening_processor):
    assert screening_processor.name_comparator("John", "John") == 1.0
    assert screening_processor.name_comparator("John", "Johnny") > 0.7
    assert screening_processor.name_comparator("John", "Smith") < 0.5
    assert screening_processor.name_comparator("John", "Jöhn") > 0.7
    assert screening_processor.name_comparator("John", "Jonh") > 0.7


def test_normalize_date(screening_processor, sample_tenant):
    assert screening_processor.normalize_date(sample_tenant.birth_date) == "1990-01-01"
    assert screening_processor.normalize_date(None) == ""


def test_exact_match(sample_tenant, sample_blacklist):
    blacklist = sample_blacklist[0]
    processor = ScreeningProcessor(sample_tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) == 100


def test_different_name_same_id(sample_tenant):
    blacklist = BlacklistMatch("Jake", "Smith", "1990-01-01", "USA", "Provider1", 90)
    processor = ScreeningProcessor(sample_tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) < 100


def test_missing_fields():
    tenant = Tenant("John", "Doe", None, None, [])
    blacklist = BlacklistMatch("John", "Doe", "1990-01-01", None, "Provider1", 50)
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) > 50


def test_blacklist_source_filtering(sample_tenant):
    blacklist = BlacklistMatch("John", "Doe", "1990-01-01", "USA", "Provider2", 90)
    processor = ScreeningProcessor(sample_tenant, [blacklist], allowed_blacklist_sources=["Provider1"])
    assert len(processor.classify_matches()) == 0


def test_case_insensitivity(screening_processor):
    assert screening_processor.name_comparator("john", "JOHN") == 1.0
    assert screening_processor.name_comparator("jOhn", "johN") == 1.0


def test_partial_match():
    tenant = Tenant("Jon", "Do", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch("John", "Doe", "1990-01-01", "USA", "Provider1", 70)
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) > 85


def test_different_date_formats(screening_processor):
    assert screening_processor.normalize_date("01/01/1990") == "1990-01-01"
    assert screening_processor.normalize_date("1990/01/01") == "1990-01-01"
    assert screening_processor.normalize_date("01-01-1990") == "1990-01-01"


def test_special_character_names():
    tenant = Tenant("Jöhn", "Döe", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch("John", "Doe", "1990-01-01", "USA", "Provider1", 80)
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) >= 85


def test_blank_names():
    tenant = Tenant("", "", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch("Jame", "Bane", "1990-01-01", "USA", "Provider1", 60)
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) < 60

def test_different_nationality(sample_tenant):
    blacklist = BlacklistMatch("John", "Doe", "1990-01-01", "UK", "Provider1", 80)
    processor = ScreeningProcessor(sample_tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) < 100

def test_empty_blacklist_entries(sample_tenant):
    processor = ScreeningProcessor(sample_tenant, [])
    assert processor.classify_matches() == []

def test_missing_birth_date(sample_tenant):
    blacklist = BlacklistMatch("John", "Doe", None, "USA", "Provider1", 75)
    processor = ScreeningProcessor(sample_tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) > 50

def test_maximum_exclusion_score():
    tenant = Tenant("John", "Doe", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch("John", "Doe", "1990-01-01", "USA", "Provider1", 100)
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) == 100

def test_case_insensitive_nationality(screening_processor):
    assert screening_processor.name_comparator("USA", "usa") == 1.0

def test_whitespace_in_names(screening_processor):
    assert screening_processor.name_comparator("John", " John ") == 1.0

def test_handle_none_values():
    tenant = Tenant(None, None, None, None, None)
    blacklist = BlacklistMatch(None, None, None, None, None, None)
    processor = ScreeningProcessor(tenant, [blacklist])
    
    assert processor.evaluate_without_ai(blacklist) > 0
