from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()

# ---------------- Individuals Table ----------------
class Individual(Base):
    __tablename__ = 'individuals'
    individual_id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    fnlwgt = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)
    hours_per_week = Column(Integer, nullable=False)
    native_country = Column(String(100), nullable=True)

    # Relationships
    employments = relationship("Employment", back_populates="individual", cascade="all, delete-orphan")
    job_details = relationship("JobDetails", back_populates="individual", cascade="all, delete-orphan")
    education_details = relationship("EducationDetails", back_populates="individual", cascade="all, delete-orphan")
    relationship_details = relationship("RelationshipDetails", back_populates="individual", cascade="all, delete-orphan")
    income_details = relationship("IncomeDetails", back_populates="individual", cascade="all, delete-orphan")

    # Validation for sex
    @validates('sex')
    def validate_sex(self, key, value):
        allowed_values = ["Male", "Female", "other"]
        if value not in allowed_values:
            raise ValueError(f"Invalid value for sex. Allowed values: {allowed_values}.")
        return value


# ---------------- Employment Table ----------------
class Employment(Base):
    __tablename__ = 'employment'
    employment_id = Column(Integer, primary_key=True, autoincrement=True)
    individual_id = Column(Integer, ForeignKey('individuals.individual_id', ondelete="CASCADE"), nullable=False)
    capital_gain = Column(Integer, default=0)
    capital_loss = Column(Integer, default=0)

    # Relationships
    individual = relationship("Individual", back_populates="employments")


# ---------------- Job Details Table ----------------
class JobDetails(Base):
    __tablename__ = 'jobdetails'
    individual_id = Column(Integer, ForeignKey('individuals.individual_id', ondelete="CASCADE"), primary_key=True)
    workclass = Column(String(50), nullable=False)
    occupation = Column(String(50), nullable=False)

    # Relationships
    individual = relationship("Individual", back_populates="job_details")


# ---------------- Education Details Table ----------------
class EducationDetails(Base):
    __tablename__ = 'educationdetails'
    individual_id = Column(Integer, ForeignKey('individuals.individual_id', ondelete="CASCADE"), primary_key=True)
    education_level = Column(String(50), nullable=False)
    education_num = Column(Integer, nullable=False)

    # Relationships
    individual = relationship("Individual", back_populates="education_details")


# ---------------- Relationship Details Table ----------------
class RelationshipDetails(Base):
    __tablename__ = 'relationshipdetails'
    individual_id = Column(Integer, ForeignKey('individuals.individual_id', ondelete="CASCADE"), primary_key=True)
    marital_status = Column(String(50), nullable=False)
    relationship_status = Column(String(50), nullable=False)

    # Relationships
    individual = relationship("Individual", back_populates="relationship_details")


# ---------------- Income Details Table ----------------
class IncomeDetails(Base):
    __tablename__ = 'incomedetails'
    individual_id = Column(Integer, ForeignKey('individuals.individual_id', ondelete="CASCADE"), primary_key=True)
    income_class = Column(String(10), nullable=False)

    # Relationships
    individual = relationship("Individual", back_populates="income_details")