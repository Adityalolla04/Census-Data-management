# End to End Project on Census Data Management with Heroku

## Project Overview

This project implements a system to manage demographic and income data, utilizing a relational PostgreSQL database. The goal is to build a predictive model to assess whether an individual makes more than $50,000 annually based on socio-economic factors like age, education, and marital status. The system also supports API operations (CRUD) and provides an interactive front-end using Streamlit.

## 1. **Introduction**

The primary objective of the system is to store, manipulate, and analyze demographic and income information to identify trends related to income inequality. The system is designed with a PostgreSQL database to manage structured data, ensuring high integrity and scalability.

### Why a Database?
A relational database is preferred over traditional Excel files due to:
- **Scalability:** Handles large datasets efficiently.
- **Data Integrity:** Enforces accuracy and consistency.
- **Concurrency:** Multiple users can access the database without conflicts.
- **Advanced Queries:** SQL allows complex data retrieval, which Excel can't handle.
  
### Target Users:
- **Researchers and Policy Analysts:** For studying earnings inequality and socio-economic trends.
- **Non-profit Organizations:** For designing programs to support underprivileged communities.

## 2. **Database Schema using PostgreSQL**

The schema consists of multiple tables capturing data related to individuals, employment, education, marital status, and income. Key tables are:

- **Individuals:** Stores personal information of individuals.
- **Employment:** Captures financial data such as capital gains/losses.
- **JobDetails:** Contains job-related data like work class and occupation.
- **EducationDetails:** Stores education level and number of schooling years.
- **RelationshipDetails:** Tracks marital status and family relationships.
- **IncomeDetails:** Stores income classification (e.g., >50K, <=50K).

### Key Relations:
- **Normalization:** The data is normalized in BCNF (Boyce-Codd Normal Form) to eliminate redundancy and ensure data consistency.
- **Foreign Keys:** The tables are linked via foreign keys, primarily using `individual_id` to maintain integrity.

### Table Creation and Insertion:
- Tables are created using SQL `CREATE TABLE` statements.
- Data insertion is handled programmatically via Python, with bulk data (215K rows) processed using normalization for efficient CRUD operations.

## 3. **API Calls (CRUD Operations)**

The system supports the following CRUD operations through an API:
- **Create:** Add new records to the database.
- **Read:** Retrieve data, e.g., income classification by age, occupation, etc.
- **Update:** Modify existing records.
- **Delete:** Remove records, with certain constraints (e.g., deletion from the `Individuals` table is not allowed).

API Design:
- API endpoints interact with the PostgreSQL database to handle CRUD operations efficiently.
- Endpoints are designed to manage demographic and income data, with proper error handling and validation.

## 4. **Streamlit App**

The front-end of the system is built using **Streamlit**, providing an interactive dashboard for users to visualize and interact with the data.

- **Dashboard:** Displays an overview of the income data with filters to fetch rows (5000 to 50,000) and allows exporting the data to Excel.
- **Manage Data:** Provides options to perform CRUD operations on various tables through the user interface.
- **Analytics Tool:** Implements bar graphs and other visualizations to analyze income distribution by various parameters such as occupation, education, and gender.

---

## Steps to Run the Project

1. **Set up PostgreSQL Database:**
   - Ensure PostgreSQL is installed and running.
   - Create the required tables using the provided SQL schema.

2. **Install Dependencies:**
   - Python libraries: `psycopg2`, `streamlit`, and others.
   - Set up Heroku for deployment.

3. **Run the Application:**
   - Run the Streamlit app for local testing or deploy it on Heroku for a live version.

4. **API Operations:**
   - Use the exposed endpoints to perform CRUD operations on the database.

---

## Conclusion

This project offers an efficient, scalable solution for demographic and income data management, incorporating modern web development practices with a robust back-end API and interactive front-end built with Streamlit. The use of Heroku for deployment ensures accessibility and scalability for real-world applications.

---

**References:**
- [Census Income Dataset](https://archive.ics.uci.edu/dataset/20/census+income)
