from typing import Optional, List

class Tenant:
    """Represents a tenant with his personal details"""

    def __init__(self,
                first_name: str,
                last_name: str,
                birth_date: Optional[str],
                nationality: Optional[str],
                id_numbers: List[str]
            ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date or ""
        self.nationality = nationality or "Unknown"
        self.id_numbers = id_numbers or []

    def __repr__(self):
        return f"Tenant(first_name={self.first_name}, last_name={self.last_name}, birth_date={self.birth_date}, nationality={self.nationality}, id_numbers={self.id_numbers})"

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "nationality": self.nationality,
            "id_numbers": self.id_numbers,
        }