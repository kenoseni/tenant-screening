def test_blacklist_match_initialization(sample_blacklist):
    blacklist_entry = sample_blacklist[0]
    assert blacklist_entry.name == "John"
    assert blacklist_entry.surname == "Doe"
    assert blacklist_entry.birth_date == "1990-01-01"
    assert blacklist_entry.provider == "ProviderX"
    assert blacklist_entry.exclusion_score == 90.0
