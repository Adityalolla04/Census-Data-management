from pydantic import BaseModel, validator
from typing import Optional


# ---------------- Individual Schemas ----------------
class IndividualBase(BaseModel):
    age: int
    fnlwgt: int
    sex: str
    hours_per_week: int
    native_country: Optional[str]


class IndividualCreate(IndividualBase):
    """Schema for creating an individual."""


class IndividualResponse(IndividualBase):
    """Schema for retrieving an individual."""
    individual_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility


# ---------------- Employment Schemas ----------------
class EmploymentBase(BaseModel):
    capital_gain: int
    capital_loss: int


class EmploymentCreate(EmploymentBase):
    """Schema for creating employment data."""
    individual_id: int


class EmploymentResponse(EmploymentBase):
    """Schema for retrieving employment data."""
    employment_id: int
    individual_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility


# ---------------- Job Details Schemas ----------------
class JobDetailsBase(BaseModel):
    workclass: str
    occupation: str


class JobDetailsCreate(JobDetailsBase):
    """Schema for creating job details."""
    individual_id: int


class JobDetailsResponse(JobDetailsBase):
    """Schema for retrieving job details."""
    individual_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility


# ---------------- Education Schemas ----------------
class EducationBase(BaseModel):
    education_level: str
    education_num: int


class EducationCreate(EducationBase):
    """Schema for creating education data."""
    individual_id: int


class EducationResponse(EducationBase):
    """Schema for retrieving education data."""
    individual_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility


# ---------------- Relationship Schemas ----------------
class RelationshipBase(BaseModel):
    marital_status: str
    relationship_status: str


class RelationshipCreate(RelationshipBase):
    """Schema for creating relationship details."""
    individual_id: int


class RelationshipResponse(RelationshipBase):
    """Schema for retrieving relationship details."""
    individual_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility


# ---------------- Income Schemas ----------------
class IncomeBase(BaseModel):
    income_class: str

    @validator("income_class")
    def validate_income_class(cls, value):
        if value not in ["<=50K", ">50K"]:
            raise ValueError("income_class must be '<=50K' or '>50K'")
        return value


class IncomeCreate(IncomeBase):
    """Schema for creating income data."""
    individual_id: int


class IncomeResponse(IncomeBase):
    """Schema for retrieving income data."""
    individual_id: int

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility