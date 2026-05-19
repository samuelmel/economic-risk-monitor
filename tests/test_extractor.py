from src.extract.world_bank_extractor import WorldBankExtractor


def test_fetch_indicator_returns_list():
    extractor = WorldBankExtractor()

    data = extractor.fetch_indicator(
        country_code="BRA",
        indicator_code="NY.GDP.MKTP.CD"
    )

    assert isinstance(data, list)


def test_fetch_indicator_has_data():
    extractor = WorldBankExtractor()

    data = extractor.fetch_indicator(
        country_code="BRA",
        indicator_code="NY.GDP.MKTP.CD"
    )

    assert len(data) > 0


def test_api_response_contains_required_keys():
    extractor = WorldBankExtractor()

    data = extractor.fetch_indicator(
        country_code="BRA",
        indicator_code="NY.GDP.MKTP.CD"
    )

    first_item = data[0]

    required_keys = {
        "countryiso3code",
        "date",
        "value",
        "country",
        "indicator",
    }

    assert required_keys.issubset(first_item.keys())