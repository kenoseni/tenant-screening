def test_tenant_initialization(sample_tenant):
    assert sample_tenant.first_name == "John"
    assert sample_tenant.last_name == "Doe"
    assert sample_tenant.birth_date == "1990-01-01"
    assert sample_tenant.nationality == "USA"
    assert sample_tenant.id_numbers == ["12345"]