DROP TABLE IF EXISTS IncomeDetails;
DROP TABLE IF EXISTS RelationshipDetails;
DROP TABLE IF EXISTS Marital;
DROP TABLE IF EXISTS EducationDetails;
DROP TABLE IF EXISTS JobDetails;
DROP TABLE IF EXISTS Employment;
DROP TABLE IF EXISTS Individuals;

CREATE TABLE Individuals (
    individual_id INT PRIMARY KEY,
    age INT NOT NULL,
    fnlwgt INT NOT NULL,
    sex VARCHAR(10) NOT NULL,
    hours_per_week INT NOT NULL,
    native_country VARCHAR(100)
);
CREATE TABLE Employment (
    employment_id INT PRIMARY KEY,
    individual_id INT NOT NULL,
    capital_gain INT DEFAULT 0,
    capital_loss INT DEFAULT 0,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);
CREATE TABLE JobDetails (
    individual_id INT PRIMARY KEY,
    workclass VARCHAR(50) NOT NULL,
    occupation VARCHAR(50) NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);
CREATE TABLE Education (
    education_id INT PRIMARY KEY,
    individual_id INT NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);
CREATE TABLE EducationDetails (
    individual_id INT PRIMARY KEY,
    education_level VARCHAR(50) NOT NULL,
    education_num INT NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);
CREATE TABLE Marital (
    marital_id INT PRIMARY KEY,
    individual_id INT NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);
CREATE TABLE RelationshipDetails (
    individual_id INT PRIMARY KEY,
    marital_status VARCHAR(50) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);
CREATE TABLE Income (
    income_id INT PRIMARY KEY,
    individual_id INT NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);
CREATE TABLE IncomeDetails (
    individual_id INT PRIMARY KEY,
    income_class VARCHAR(10) NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
);

