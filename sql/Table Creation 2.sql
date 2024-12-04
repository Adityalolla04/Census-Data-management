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
    individual_id INT,
    workclass VARCHAR(50) NOT NULL,
    occupation VARCHAR(50) NOT NULL,
    capital_gain INT DEFAULT 0,
    capital_loss INT DEFAULT 0,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
        ON DELETE CASCADE
);

CREATE TABLE Education (
    education_id INT PRIMARY KEY,
    individual_id INT,
    education_level VARCHAR(50) NOT NULL,
    education_num INT NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
        ON DELETE CASCADE
);

CREATE TABLE Marital_Status (
    marital_id INT  PRIMARY KEY,
    individual_id INT,
    marital_status VARCHAR(50) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
        ON DELETE CASCADE
);

CREATE TABLE Income (
    income_id INT  PRIMARY KEY,
    individual_id INT,
    income_class VARCHAR(5) NOT NULL,
    CHECK (income_class IN ('<=50K', '>50K')),
    FOREIGN KEY (individual_id) REFERENCES Individuals(individual_id)
        ON DELETE CASCADE
);






