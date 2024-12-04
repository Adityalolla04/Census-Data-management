Insertion of Data:
•	Inserted the data with the help of Python Implementation process as there are bulk data of 215K rows.
•	Preprocessed Data: The data is preprocessed by removing the null values
•	Database Connection: The data base connection is written with the Postgres URL to the Census Data
•	Insertion: The data is inserted by normalization procedure into BCNF for the better output and to perform the CRUD operations in the API.

E/R Diagram Details:
Central Entity: individual

The individual table is the central entity, with attributes including age, sex, hours worked per week, and native country.
It connects to several other entities via foreign keys, making it the backbone of the database.
Key Relationships:

The diagram clearly defines the following relationships between individuals and other entities:
Education: Outlines education levels linked to individuals via the individual_id. It also captures education levels and numerical education scores.
Employment: Relates persons and captures information such as capital gain and capital loss.
Income: Maintains individual income information and is related by the individual_id.
IncomeDetails: Adds classification of income, such as income class, based on income_id.
JobDetails: Captures job-specific information such as work class and occupation.
Marital: Maintains marital status of individuals, related by the individual_id.
RelationshipDetails: Specific relationship statuses related to individual_id.

Normalization:
The database seems normalized, with very minimal data redundancy.
The attributes are stored in respective entities and related through foreign keys, which helps in maintaining a structured design.
Primary and Foreign Keys:

There is a primary key (PK) for each entity, which ensures that no record is duplicated.
Foreign key (FK) constraints relate the entities and maintain referential integrity.
Focus on Demographic and Economic Data:

This diagram appears to be focused on demographic and economic attributes of the individuals, such as:

Employment information, including but not limited to capital gain/loss.
Educational background and levels.
Income classification.
Work and relationship details.
Potential Use Cases:

This structure is appropriate for demographic analysis, income prediction models, or labor market analysis.
It can also support advanced queries on the relationships between education, employment, and income.

Strengths:
Modular structure: Each aspect of a person's profile, such as education, job, and marital status, is well-separated.
Scalability: New entities, such as health or geographic details, can be added with ease.
Data integrity: Relationships and keys ensure that data is consistent and accurate.