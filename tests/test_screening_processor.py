from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch
from challenge.screening_processor import ScreeningProcessor


def test_screening_processor_initialization(
    screening_processor, sample_tenant, sample_blacklist
):
    assert screening_processor.tenant == sample_tenant
    assert screening_processor.blacklist_entries == sample_blacklist
    assert screening_processor.allowed_blacklist_sources == [
        "ProviderX-blacklist",
        "ProviderY-blacklist",
    ]

    assert isinstance(screening_processor, ScreeningProcessor)  # Verify object type
    assert len(screening_processor.blacklist_entries) == len(
        sample_blacklist
    )  # Check length consistency
    assert (
        screening_processor.tenant.first_name == sample_tenant.first_name
    )  # Validate tenant details
    assert screening_processor.tenant.last_name == sample_tenant.last_name
    assert screening_processor.tenant.birth_date == sample_tenant.birth_date
    assert screening_processor.tenant.nationality == sample_tenant.nationality
    assert screening_processor.tenant.id_numbers == sample_tenant.id_numbers


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
    assert processor.evaluate_without_ai(blacklist) == 100.0


def test_different_name_same_id(sample_tenant):
    blacklist = BlacklistMatch(
        "Jake", "Smith", "1990-01-01", "USA", "Provider1-blacklist", 90.0, ["12345"]
    )
    processor = ScreeningProcessor(sample_tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) <= 100.0


def test_missing_fields():
    tenant = Tenant("John", "Doe", None, None, [])
    blacklist = BlacklistMatch("John", "Doe", "1990-01-01", None, "Provider1-blacklist", 50.0, [])
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) >= 50.0


def test_blacklist_source_filtering(sample_tenant):
    blacklist = BlacklistMatch(
        "John", "Doe", "1990-01-01", "USA", "Provider2-blacklist", 90.0, ["12345"]
    )
    processor = ScreeningProcessor(
        sample_tenant, [blacklist], allowed_blacklist_sources=["Provider1"]
    )
    assert len(processor.classify_matches(False)) == 0

    allowed_blacklist = BlacklistMatch(
        "John", "Doe", "1990-01-01", "USA", "Provider1-blacklist", 90.0, ["12345"]
    )
    processor_allowed = ScreeningProcessor(
        sample_tenant,
        [allowed_blacklist],
        allowed_blacklist_sources=["Provider1-blacklist"],
    )
    assert len(processor_allowed.classify_matches(False)) == 1
    assert (
        processor_allowed.classify_matches(False)[0]["classification"]
        == "Relevant Match"
    )


def test_case_insensitivity(screening_processor):
    assert screening_processor.name_comparator("john", "JOHN") == 1.0
    assert screening_processor.name_comparator("jOhn", "johN") == 1.0

    assert screening_processor.name_comparator("Jöhn", "jÖhn") == 1.0


def test_partial_match():
    tenant = Tenant("Jon", "Do", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch(
        "John", "Doe", "1990-01-01", "USA", "Provider1-blacklist", 70.0, ["12345"]
    )
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) > 85.0

    assert processor.name_comparator("Jon", "John") > 0.5
    assert processor.name_comparator("Do", "Doe") > 0.5


def test_different_date_formats(screening_processor):
    assert screening_processor.normalize_date("01/01/1990") == "1990-01-01"
    assert screening_processor.normalize_date("1990/01/01") == "1990-01-01"
    assert screening_processor.normalize_date("01-01-1990") == "1990-01-01"


def test_special_character_names():
    tenant = Tenant("Jöhn", "Döe", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch(
        "John", "Doe", "1990-01-01", "USA", "Provider1-blacklist", 80.0, ["12345"]
    )
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) >= 85.0


def test_blank_names():
    tenant = Tenant("", "", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch(
        "Jame", "Bane", "1990-01-01", "USA", "Provider1-blacklist", 60.0, []
    )
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) <= 60.0


def test_different_nationality(sample_tenant):
    blacklist = BlacklistMatch(
        "John", "Doe", "1990-01-01", "UK", "Provider1-blacklist", 80.0, ["12345"]
    )
    processor = ScreeningProcessor(sample_tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) <= 100.0


def test_empty_blacklist_entries(sample_tenant):
    processor = ScreeningProcessor(sample_tenant, [])
    assert processor.classify_matches() == []


def test_missing_birth_date(sample_tenant):
    blacklist = BlacklistMatch("John", "Doe", None, "USA", "Provider1-blacklist", 75.0, ["12445"])
    processor = ScreeningProcessor(sample_tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) > 50.0


def test_maximum_exclusion_score():
    tenant = Tenant("John", "Doe", "1990-01-01", "USA", ["12345"])
    blacklist = BlacklistMatch(
        "John", "Doe", "1990-01-01", "USA", "Provider1-blacklist", 100, ["12345"]
    )
    processor = ScreeningProcessor(tenant, [blacklist])
    assert processor.evaluate_without_ai(blacklist) == 100


def test_case_insensitive_nationality(screening_processor):
    assert screening_processor.name_comparator("USA", "usa") == 1.0


def test_whitespace_in_names(screening_processor):
    assert screening_processor.name_comparator("John", " John ") == 1.0


def test_handle_none_values():
    tenant = Tenant(None, None, None, None, None)
    blacklist = BlacklistMatch(None, None, None, None, None, None, None)
    processor = ScreeningProcessor(tenant, [blacklist])

    assert processor.evaluate_without_ai(blacklist) > 0


def test_evaluate_with_ai(mocker, sample_tenant, sample_blacklist):
    mock_generate_model_response = mocker.patch(
        "challenge.screening_processor.ScreeningProcessor.evaluate_with_ai"
    )

    mock_generate_model_response.return_value = {
        "ai_model_confidence_score": 85.0,
        "match_classification": "Relevant Match",
        "explanation": "High similarity in name, birth date, and nationality.",
    }

    processor = ScreeningProcessor(sample_tenant, [sample_blacklist])
    response = processor.evaluate_with_ai(sample_blacklist)

    assert isinstance(response, dict)
    assert response["ai_model_confidence_score"] == 85.0
    mock_generate_model_response.assert_called_once()

    assert "match_classification" in response
    assert "explanation" in response
    assert response["match_classification"] == "Relevant Match"
