from typing import Optional, List


class BlacklistMatch:
    """Represents the one entry of the search result(a blacklist entry) with details about the searched entity"""

    def __init__(
        self,
        name: str,
        surname: str,
        birth_date: Optional[str],
        birth_country: Optional[str],
        provider: str,
        exclusion_score: float,
        identification_number: List[str],
    ):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date or ""
        self.birth_country = birth_country or "Unknown"
        self.provider = provider
        self.exclusion_score = exclusion_score or 0.0
        self.identification_number = identification_number or []

    def __repr__(self):
        return f"BlacklistMatch(name={self.name}, surname={self.surname}, birth_date={self.birth_date}, birth_country={self.birth_country}, provider={self.provider}, exclusion_score={self.exclusion_score})"
