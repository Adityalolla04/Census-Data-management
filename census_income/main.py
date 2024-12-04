from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import operations, schemas, models

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Census Income API."}


# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Utility for Validation ----------------
def validate_individual(db: Session, individual_id: int):
    """Validate if an individual exists."""
    individual = db.query(models.Individual).filter(models.Individual.individual_id == individual_id).first()
    if not individual:
        raise HTTPException(status_code=404, detail="Individual not found")


# ---------------- Individuals Endpoints ----------------
@app.post("/individuals/", response_model=schemas.IndividualResponse)
def create_individual(individual: schemas.IndividualCreate, db: Session = Depends(get_db)):
    return operations.create_individual(db, individual)


@app.get("/individuals/", response_model=list[schemas.IndividualResponse])
def get_individuals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return operations.get_individuals(db, skip, limit)


@app.get("/individuals/{individual_id}", response_model=schemas.IndividualResponse)
def get_individual(individual_id: int, db: Session = Depends(get_db)):
    return operations.get_individual(db, individual_id)


@app.put("/individuals/{individual_id}", response_model=schemas.IndividualResponse)
def update_individual(individual_id: int, individual: schemas.IndividualCreate, db: Session = Depends(get_db)):
    return operations.update_individual(db, individual_id, individual)


# ---------------- Job Details Endpoints ----------------
@app.post("/jobdetails/", response_model=schemas.JobDetailsResponse)
def create_job_details(job_details: schemas.JobDetailsCreate, db: Session = Depends(get_db)):
    validate_individual(db, job_details.individual_id)
    return operations.create_job_details(db, job_details)

# Fetch all job details
@app.get("/jobdetails/", response_model=list[schemas.JobDetailsResponse])
def get_all_job_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.JobDetails).offset(skip).limit(limit).all()


@app.get("/jobdetails/{individual_id}", response_model=schemas.JobDetailsResponse)
def get_job_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.get_job_details(db, individual_id)


@app.put("/jobdetails/{individual_id}", response_model=schemas.JobDetailsResponse)
def update_job_details(individual_id: int, job_details: schemas.JobDetailsCreate, db: Session = Depends(get_db)):
    return operations.update_job_details(db, individual_id, job_details)


@app.delete("/jobdetails/{individual_id}")
def delete_job_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.delete_job_details(db, individual_id)


# ---------------- Education Details Endpoints ----------------
@app.post("/educationdetails/", response_model=schemas.EducationResponse)
def create_education_details(education_details: schemas.EducationCreate, db: Session = Depends(get_db)):
    validate_individual(db, education_details.individual_id)
    return operations.create_education_details(db, education_details)

@app.get("/educationdetails/", response_model=list[schemas.EducationResponse])
def get_education_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.EducationDetails).offset(skip).limit(limit).all()


@app.get("/educationdetails/{individual_id}", response_model=schemas.EducationResponse)
def get_education_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.get_education_details(db, individual_id)


@app.put("/educationdetails/{individual_id}", response_model=schemas.EducationResponse)
def update_education_details(individual_id: int, education_details: schemas.EducationCreate, db: Session = Depends(get_db)):
    return operations.update_education_details(db, individual_id, education_details)


@app.delete("/educationdetails/{individual_id}")
def delete_education_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.delete_education_details(db, individual_id)


# ---------------- Income Details Endpoints ----------------
@app.post("/incomedetails/", response_model=schemas.IncomeResponse)
def create_income_details(income_details: schemas.IncomeCreate, db: Session = Depends(get_db)):
    validate_individual(db, income_details.individual_id)
    return operations.create_income_details(db, income_details)


@app.get("/incomedetails/{individual_id}", response_model=schemas.IncomeResponse)
def get_income_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.get_income_details(db, individual_id)

@app.get("/incomedetails/", response_model=list[schemas.IncomeResponse])
def get_income_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.IncomeDetails).offset(skip).limit(limit).all()


@app.put("/incomedetails/{individual_id}", response_model=schemas.IncomeResponse)
def update_income_details(individual_id: int, income_details: schemas.IncomeCreate, db: Session = Depends(get_db)):
    return operations.update_income_details(db, individual_id, income_details)


@app.delete("/incomedetails/{individual_id}")
def delete_income_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.delete_income_details(db, individual_id)


# ---------------- Relationship Details Endpoints ----------------
@app.post("/relationshipdetails/", response_model=schemas.RelationshipResponse)
def create_relationship_details(relationship_details: schemas.RelationshipCreate, db: Session = Depends(get_db)):
    validate_individual(db, relationship_details.individual_id)
    return operations.create_relationship_details(db, relationship_details)

@app.get("/relationshipdetails/", response_model=list[schemas.RelationshipResponse])
def get_relationship_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.RelationshipDetails).offset(skip).limit(limit).all()

@app.get("/relationshipdetails/{individual_id}", response_model=schemas.RelationshipResponse)
def get_relationship_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.get_relationship_details(db, individual_id)


@app.put("/relationshipdetails/{individual_id}", response_model=schemas.RelationshipResponse)
def update_relationship_details(individual_id: int, relationship_details: schemas.RelationshipCreate, db: Session = Depends(get_db)):
    return operations.update_relationship_details(db, individual_id, relationship_details)


@app.delete("/relationshipdetails/{individual_id}")
def delete_relationship_details(individual_id: int, db: Session = Depends(get_db)):
    return operations.delete_relationship_details(db, individual_id)