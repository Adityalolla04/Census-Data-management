DROP INDEX IF EXISTS idx_individual_id_individuals;
CREATE INDEX idx_individual_id_individuals ON Individuals(individual_id);

DROP INDEX IF EXISTS idx_individual_id_employment;
CREATE INDEX idx_individual_id_employment ON Employment(individual_id);

DROP INDEX IF EXISTS idx_individual_id_jobdetails;
CREATE INDEX idx_individual_id_jobdetails ON JobDetails(individual_id);

DROP INDEX IF EXISTS idx_individual_id_educationdetails;
CREATE INDEX idx_individual_id_educationdetails ON EducationDetails(individual_id);

DROP INDEX IF EXISTS idx_individual_id_relationshipdetails;
CREATE INDEX idx_individual_id_relationshipdetails ON RelationshipDetails(individual_id);

DROP INDEX IF EXISTS idx_income_class;
CREATE INDEX idx_income_class ON IncomeDetails(income_class);

DROP INDEX IF EXISTS idx_workclass;
CREATE INDEX idx_workclass ON JobDetails(workclass);

DROP INDEX IF EXISTS idx_occupation;
CREATE INDEX idx_occupation ON JobDetails(occupation);

DROP INDEX IF EXISTS idx_capital_gain;
CREATE INDEX idx_capital_gain ON Employment(capital_gain);
