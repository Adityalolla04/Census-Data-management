from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


# Utility for handling not found errors
def handle_not_found(entity: str):
    raise HTTPException(status_code=404, detail=f"{entity} not found")

# Individuals
def create_individual(db: Session, individual: schemas.IndividualCreate):
    """Create a new individual."""
    new_individual = models.Individual(**individual.dict())
    db.add(new_individual)
    db.commit()
    db.refresh(new_individual)
    return new_individual


def get_individuals(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all individuals with pagination."""
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="skip and limit must be non-negative integers.")
    return db.query(models.Individual).offset(skip).limit(limit).all()


def get_individual(db: Session, individual_id: int):
    """Retrieve an individual by ID."""
    individual = db.query(models.Individual).filter(models.Individual.individual_id == individual_id).first()
    if not individual:
        handle_not_found("Individual")
    return individual


def update_individual(db: Session, individual_id: int, individual: schemas.IndividualCreate):
    """Update an individual's details."""
    db_individual = db.query(models.Individual).filter(models.Individual.individual_id == individual_id).first()
    if not db_individual:
        handle_not_found("Individual")
    for key, value in individual.dict(exclude_unset=True).items():
        setattr(db_individual, key, value)
    db.commit()
    db.refresh(db_individual)
    return db_individual

# Job Details
def create_job_details(db: Session, job_details: schemas.JobDetailsCreate):
    """Create or update job details for an individual."""
    db_job_details = db.query(models.JobDetails).filter(models.JobDetails.individual_id == job_details.individual_id).first()
    if db_job_details:
        # Update existing job details
        for key, value in job_details.dict(exclude_unset=True).items():
            setattr(db_job_details, key, value)
        db.commit()
        db.refresh(db_job_details)
        return db_job_details
    else:
        # Create new job details
        new_job_details = models.JobDetails(**job_details.dict())
        db.add(new_job_details)
        db.commit()
        db.refresh(new_job_details)
        return new_job_details


def get_all_job_details(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all job details with pagination."""
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="skip and limit must be non-negative integers.")
    return db.query(models.JobDetails).offset(skip).limit(limit).all()


def get_job_details(db: Session, individual_id: int):
    """Retrieve job details by individual ID."""
    job_details = db.query(models.JobDetails).filter(models.JobDetails.individual_id == individual_id).first()
    if not job_details:
        handle_not_found("JobDetails")
    return job_details


def update_job_details(db: Session, individual_id: int, job_details: schemas.JobDetailsCreate):
    """Update job details by individual ID."""
    db_job_details = db.query(models.JobDetails).filter(models.JobDetails.individual_id == individual_id).first()
    if not db_job_details:
        handle_not_found("JobDetails")
    for key, value in job_details.dict(exclude_unset=True).items():
        setattr(db_job_details, key, value)
    db.commit()
    db.refresh(db_job_details)
    return db_job_details


def delete_job_details(db: Session, individual_id: int):
    """Delete job details by individual ID."""
    db_job_details = db.query(models.JobDetails).filter(models.JobDetails.individual_id == individual_id).first()
    if not db_job_details:
        handle_not_found("JobDetails")
    db.delete(db_job_details)
    db.commit()
    return {"message": "Job details deleted successfully"}

# EducationDetails 
from sqlalchemy.exc import IntegrityError

def create_education_details(db: Session, education_details: schemas.EducationCreate):
    """Create or update education details for an individual."""
    try:
        # Try to create new education details
        new_education_details = models.EducationDetails(**education_details.dict())
        db.add(new_education_details)
        db.commit()
        db.refresh(new_education_details)
        return new_education_details
    except IntegrityError:
        # Rollback the transaction in case of conflict
        db.rollback()
        
        # Fetch and update the existing record
        existing_record = db.query(models.EducationDetails).filter_by(
            individual_id=education_details.individual_id
        ).first()
        if existing_record:
            # Update the existing record's details
            existing_record.education_level = education_details.education_level
            existing_record.education_num = education_details.education_num
            
            # Commit the update
            db.commit()
            db.refresh(existing_record)
            return existing_record
        else:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error: could not create or update education details."
            )

def get_all_education_details(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all education details with pagination."""
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="skip and limit must be non-negative integers.")
    return db.query(models.EducationDetails).offset(skip).limit(limit).all()


def get_education_details(db: Session, individual_id: int):
    """Retrieve education details by individual ID."""
    education_details = db.query(models.EducationDetails).filter(models.EducationDetails.individual_id == individual_id).first()
    if not education_details:
        handle_not_found("EducationDetails")
    return education_details


def update_education_details(db: Session, individual_id: int, education_details: schemas.EducationCreate):
    """Update education details by individual ID."""
    db_education_details = db.query(models.EducationDetails).filter(models.EducationDetails.individual_id == individual_id).first()
    if not db_education_details:
        handle_not_found("EducationDetails")
    for key, value in education_details.dict(exclude_unset=True).items():
        setattr(db_education_details, key, value)
    db.commit()
    db.refresh(db_education_details)
    return db_education_details


def delete_education_details(db: Session, individual_id: int):
    """Delete education details by individual ID."""
    db_education_details = db.query(models.EducationDetails).filter(models.EducationDetails.individual_id == individual_id).first()
    if not db_education_details:
        handle_not_found("EducationDetails")
    db.delete(db_education_details)
    db.commit()
    return {"message": "Education details deleted successfully"}


def create_relationship_details(db: Session, relationship_details: schemas.RelationshipCreate):
    """Create or update relationship details for an individual."""
    try:
        # Attempt to create new relationship details
        new_relationship_details = models.RelationshipDetails(**relationship_details.dict())
        db.add(new_relationship_details)
        db.commit()
        db.refresh(new_relationship_details)
        return new_relationship_details
    except IntegrityError:
        # Rollback transaction in case of conflict
        db.rollback()

        # Fetch and update the existing record
        existing_record = db.query(models.RelationshipDetails).filter_by(
            individual_id=relationship_details.individual_id
        ).first()
        if existing_record:
            # Update the existing record's details
            existing_record.marital_status = relationship_details.marital_status
            existing_record.relationship = relationship_details.relationship_status

            # Commit the update
            db.commit()
            db.refresh(existing_record)
            return existing_record
        else:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error: could not create or update relationship details."
            )



def get_all_relationship_details(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all relationship details with pagination."""
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="skip and limit must be non-negative integers.")
    return db.query(models.RelationshipDetails).offset(skip).limit(limit).all()


def get_relationship_details(db: Session, individual_id: int):
    """Retrieve relationship details by individual ID."""
    relationship_details = db.query(models.RelationshipDetails).filter(models.RelationshipDetails.individual_id == individual_id).first()
    if not relationship_details:
        handle_not_found("RelationshipDetails")
    return relationship_details


def update_relationship_details(db: Session, individual_id: int, relationship_details: schemas.RelationshipCreate):
    """Update relationship details by individual ID."""
    db_relationship_details = db.query(models.RelationshipDetails).filter(models.RelationshipDetails.individual_id == individual_id).first()
    if not db_relationship_details:
        handle_not_found("RelationshipDetails")
    for key, value in relationship_details.dict(exclude_unset=True).items():
        setattr(db_relationship_details, key, value)
    db.commit()
    db.refresh(db_relationship_details)
    return db_relationship_details


def delete_relationship_details(db: Session, individual_id: int):
    """Delete relationship details by individual ID."""
    db_relationship_details = db.query(models.RelationshipDetails).filter(models.RelationshipDetails.individual_id == individual_id).first()
    if not db_relationship_details:
        handle_not_found("RelationshipDetails")
    db.delete(db_relationship_details)
    db.commit()
    return {"message": "Relationship details deleted successfully"}

# IncomeDetails
def create_income_details(db: Session, income_details: schemas.IncomeCreate):
    """Create income details for an individual."""
    try:
        # Try to create new income details
        new_income_details = models.IncomeDetails(**income_details.dict())
        db.add(new_income_details)
        db.commit()
        db.refresh(new_income_details)
        return new_income_details
    except IntegrityError:
        # Rollback the transaction in case of conflict
        db.rollback()

        # Fetch and update the existing record
        existing_record = db.query(models.IncomeDetails).filter_by(
            individual_id=income_details.individual_id
        ).first()
        if existing_record:
            # Update the existing record's income_class
            existing_record.income_class = income_details.income_class
            
            # Commit the update
            db.commit()
            db.refresh(existing_record)
            return existing_record
        else:
            raise HTTPException(
                status_code=500,
                detail="Unexpected error: could not create or update income details."
            )



def get_income_details(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all income details with pagination."""
    return db.query(models.IncomeDetails).offset(skip).limit(limit).all()


def get_income_details(db: Session, individual_id: int):
    """Retrieve income details by individual ID."""
    income_details = db.query(models.IncomeDetails).filter(models.IncomeDetails.individual_id == individual_id).first()
    if not income_details:
        handle_not_found("IncomeDetails")
    return income_details


def update_income_details(db: Session, individual_id: int, income_details: schemas.IncomeCreate):
    """Update income details by individual ID."""
    db_income_details = db.query(models.IncomeDetails).filter(models.IncomeDetails.individual_id == individual_id).first()
    if not db_income_details:
        handle_not_found("IncomeDetails")
    for key, value in income_details.dict(exclude_unset=True).items():
        setattr(db_income_details, key, value)
    db.commit()
    db.refresh(db_income_details)
    return db_income_details


def delete_income_details(db: Session, individual_id: int):
    """Delete income details by individual ID."""
    db_income_details = db.query(models.IncomeDetails).filter(models.IncomeDetails.individual_id == individual_id).first()
    if not db_income_details:
        handle_not_found("IncomeDetails")
    db.delete(db_income_details)
    db.commit()
    return {"message": "Income details deleted successfully"}