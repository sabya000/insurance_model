from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tier import tier_1_cities, tier_2_cities

# =========================
# Input Schema
# =========================
class UserInput(BaseModel):

    age: Annotated[
        int,
        Field(gt=0, lt=120)
    ]

    weight: Annotated[
        float,
        Field(gt=0)
    ]

    height: Annotated[
        float,
        Field(gt=0)
    ]

    income_lpa: Annotated[
        float,
        Field(gt=0)
    ]

    smoker: bool

    city: str

    occupation: Literal[
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]

    @field_validator('city')
    @classmethod
    def normalie_city(cls, v: str)-> str:
        v = v.strip().title()
        return v


    # =========================
    # Computed Fields
    # =========================

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def life_risk(self) -> str:

        if self.smoker and self.bmi > 30:
            return "high"

        elif self.smoker or self.bmi > 27:
            return "medium"

        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:

        if self.age < 25:
            return "young"

        elif self.age < 45:
            return "adult"

        elif self.age < 60:
            return "middle_aged"

        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:

        if self.city in tier_1_cities:
            return 1

        elif self.city in tier_2_cities:
            return 2

        return 3
