import re
import json
from datetime import datetime
from difflib import SequenceMatcher
from typing import List, Dict
from challenge.tenant import Tenant
from challenge.black_list_match import BlacklistMatch
from challenge.ai_prompt import ai_prompt
from challenge.model import (
    generate_model_response,
    generate_model_response_with_open_ai,
)
from challenge.utils import clean_string

# Constants
INITIAL_SCORE = 0.0
FIFTEEN = 15.0
TWENTY = 20.0
THIRTY = 30.0
FORTY = 40.0


class ScreeningProcessor:
    """Pre-assessing the search result(blacklist entries) given the information a person provided(tenants information) to determine potential matches."""

    def __init__(
        self,
        tenant: Tenant,
        blacklist_entries: List[BlacklistMatch],
        allowed_blacklist_sources: List[str] = None,
    ):
        self.tenant = tenant
        self.blacklist_entries = blacklist_entries
        self.allowed_blacklist_sources = allowed_blacklist_sources or []

    def __repr__(self):
        return f"ScreeningProcessor(tenant={self.tenant}, blacklist_entries={self.blacklist_entries}, allowed_blacklist_sources={self.allowed_blacklist_sources})"

    def name_comparator(self, name1: str, name2: str) -> float:
        """Calculates the similarity between two names using SequenceMatcher"""
        return SequenceMatcher(None, clean_string(name1), clean_string(name2)).ratio()

    def normalize_date(self, date: str) -> str:
        """Ensure birth dates are in YYYY-MM-DD format"""

        if not date:
            return ""

        date = date.strip()
        date_formats = ["%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%Y-%m-%d"]

        for fmt in date_formats:
            try:
                return datetime.strptime(date, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue

        raise ValueError(f"Unknown date format: {date}")

    def evaluate_without_ai(self, blacklist_entry: BlacklistMatch) -> float:
        """Evaluate the match confidence score based on multiple factors"""
        score = INITIAL_SCORE
        print("**********************", self.tenant.first_name)
        tenant_names = re.split(
            r"\s+", clean_string(self.tenant.first_name)
        ) + re.split(r"\s+", clean_string(self.tenant.last_name))
        blacklist_names = re.split(
            r"\s+", clean_string(blacklist_entry.name)
        ) + re.split(r"\s+", clean_string(blacklist_entry.surname))

        name_match_score = max(
            self.name_comparator(tenant_name, blacklist_name)
            for tenant_name in tenant_names
            for blacklist_name in blacklist_names
        )

        # Name similarity
        if name_match_score > 0.9:
            # High name similarity
            score += THIRTY
        elif name_match_score > 0.7:
            # Medium name similarity
            score += FIFTEEN

        # Birth date match
        if (
            self.tenant.birth_date
            and blacklist_entry.birth_date
            and self.normalize_date(self.tenant.birth_date)
            == self.normalize_date(blacklist_entry.birth_date)
        ):
            score += FORTY

        # Nationality factor
        if clean_string(self.tenant.nationality) == clean_string(
            blacklist_entry.birth_country
        ):
            score += TWENTY
        # Exclusion match score from provider
        if blacklist_entry.exclusion_score >= 85.0:
            score += THIRTY
        elif blacklist_entry.exclusion_score >= 70.0:
            score += FIFTEEN

        id_match_score = (
            max(
                SequenceMatcher(None, tenant_id, blacklist_id).ratio()
                for tenant_id in self.tenant.id_numbers
                for blacklist_id in blacklist_entry.identification_number
            )
            if self.tenant.id_numbers and blacklist_entry.identification_number
            else 0
        )

        if id_match_score > 0.8:
            score += THIRTY  # Strong match
        elif id_match_score > 0.6:
            score += FIFTEEN  # Moderate match

        return min(score, 100.0)

    def evaluate_with_ai(
        self, blacklist_entry: BlacklistMatch, use_chat_gpt=True
    ) -> Dict:
        """Uses an AI model to determine the likelihood of a true match, the default model is CHAT_GPT"""

        prompt = ai_prompt(self.tenant, blacklist_entry)

        if use_chat_gpt:
            response = generate_model_response_with_open_ai(prompt)
        else:
            response = generate_model_response(prompt)

        return response

    def classify_matches(self, use_ai=True) -> List[Dict]:
        """Classification outcome per tenant entry based on evaluated score"""
        results = []

        for entry in self.blacklist_entries:
            if (
                self.allowed_blacklist_sources
                and entry.provider not in self.allowed_blacklist_sources
            ):
                continue
            if use_ai:
                ai_assessment = self.evaluate_with_ai(entry) or {}
                if ai_assessment.get("match_classification") != "Error":
                    match_score = min(
                        ai_assessment.get("ai_model_confidence_score", 0), 100.0
                    )
                    results.append(
                        {
                            "name": entry.name,
                            "surname": entry.surname,
                            "match_score": match_score,
                            "classification": ai_assessment.get(
                                "match_classification", "Probably Not Relevant"
                            ),
                            "explanation": ai_assessment.get(
                                "explanation", "No explanation provided"
                            ),
                        }
                    )
            else:
                # Fallback mechanism without AI
                match_score = self.evaluate_without_ai(entry)
                classification = "Probably Not Relevant"
                if match_score >= 85.0:
                    classification = "Relevant Match"
                elif match_score >= 65.0:
                    classification = "Needs Review"

                results.append(
                    {
                        "name": entry.name,
                        "surname": entry.surname,
                        "match_score": match_score,
                        "classification": classification,
                    }
                )

        print(json.dumps(results, indent=4))
        return results

    @staticmethod
    def extract_blacklist_matches(pipeline: List[Dict]) -> List[BlacklistMatch]:
        """Extract blacklist matches from the pipeline step dynamically"""

        blacklist_entries = []
        for step in pipeline:
            if step.get("type", "").endswith("blacklist"):
                result = step.get("result", {}).get("data", {})
                if result.get("found", False):
                    for match in result.get("matches", []):
                        blacklist_entries.append(
                            BlacklistMatch(
                                name=match.get("name", ""),
                                surname=match.get("surname", ""),
                                birth_date=match.get("birthDate"),
                                birth_country=match.get("birthCountry", ""),
                                provider=match.get("providerId", ""),
                                exclusion_score=match.get("exclusionMatchScore", 0),
                                identification_number=match.get(
                                    "identificationNumber", []
                                ),
                            )
                        )
        return blacklist_entries

    @classmethod
    def from_pipeline(
        cls,
        tenant: Tenant,
        pipeline: List[Dict],
        allowed_blacklist_sources: List[str] = None,
    ):
        blacklist_entries = cls.extract_blacklist_matches(pipeline)
        return cls(tenant, blacklist_entries, allowed_blacklist_sources)
