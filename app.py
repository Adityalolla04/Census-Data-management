import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from sqlalchemy import text
from census_income.database import SessionLocal
from io import BytesIO
import matplotlib.pyplot as plt
openpyxl


# Set page configuration
st.set_page_config(
    page_title="Census Income Management System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fetch combined data from the database with filtering
def fetch_combined_data(min_rows, max_rows):
    query = text("""
        SELECT 
    i.individual_id, i.age, i.sex, i.fnlwgt, i.hours_per_week, i.native_country,
    jd.workclass, jd.occupation, ed.education_level, ed.education_num, 
    inc.income_class, rel.marital_status
    FROM 
        individuals i
    LEFT JOIN 
        jobdetails jd ON i.individual_id = jd.individual_id
    LEFT JOIN 
        educationdetails ed ON i.individual_id = ed.individual_id
    LEFT JOIN 
        incomedetails inc ON i.individual_id = inc.individual_id
    LEFT JOIN 
        relationshipdetails rel ON i.individual_id = rel.individual_id
    WHERE 
        inc.income_class = '>50K'
    ORDER BY 
        individual_id
    LIMIT :max_rows OFFSET :min_rows
    """)
    try:
        with SessionLocal() as db:
            result = db.execute(query, {"max_rows": max_rows, "min_rows": min_rows})
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        st.error(f"Error fetching data from database: {e}")
        return pd.DataFrame()

# Fetch data from FastAPI
def fetch_data(endpoint):
    BASE_URL = "http://127.0.0.1:8000/"
    try:
        response = requests.get(BASE_URL + endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data from {endpoint}. Status: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Delete data from FastAPI
def delete_data(endpoint):
    BASE_URL = "http://127.0.0.1:8000/"
    try:
        response = requests.delete(BASE_URL + endpoint)
        if response.status_code == 200:
            st.success("Record successfully deleted!")
        else:
            st.error(f"Failed to delete record: {response.text}")
    except Exception as e:
        st.error(f"Error deleting data: {e}")

# Export Data to Excel
def export_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="CensusData")
    output.seek(0)
    return output

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Dashboard", "Manage Data", "Data Analysis"])

# Field Options for Dropdowns
WORKCLASS_OPTIONS = ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"]
MARITAL_STATUS_OPTIONS = ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"]
EDUCATION_OPTIONS = ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"]
RELATIONSHIP_OPTIONS = ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"]

# Dashboard Section
if menu == "Dashboard":
    st.title("Dashboard: Census Income Management System")

    st.sidebar.header("Filter Data")
    min_rows = st.sidebar.number_input("Minimum Rows (Offset)", value=0, min_value=0, step=500)
    max_rows = st.sidebar.number_input("Maximum Rows (Limit)", value=5000, min_value=1, step=500)

    combined_data = fetch_combined_data(min_rows, max_rows)
    if not combined_data.empty:
        st.header("Overview Metrics")
        avg_age = combined_data['age'].mean()
        income_greater_50k = len(combined_data[combined_data["income_class"] == ">50K"])

        col1, col2 = st.columns(2)
        col1.metric("Average Age", round(avg_age, 2))
        col2.metric("Income >50K", income_greater_50k)

        st.header(f"Filtered Data ({min_rows} - {max_rows} Rows)")
        st.dataframe(combined_data)

        st.download_button(
            label="Download Data as Excel",
            data=export_to_excel(combined_data),
            file_name="census_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# Manage Data Section
elif menu == "Manage Data":
    st.title("Manage Census Data")

    table_options = ["individuals", "jobdetails", "educationdetails", "incomedetails", "relationshipdetails"]
    selected_table = st.sidebar.selectbox("Select Table to Manage", table_options)

    st.header(f"Manage {selected_table.capitalize()} Data")

    # Fetch individual IDs for dropdown
    individual_data = fetch_data("individuals/")
    if individual_data:
        individual_ids = [item["individual_id"] for item in individual_data]
    else:
        individual_ids = []

    # Fetch Data by Individual ID
    st.subheader(f"Fetch Data by Individual ID")
    selected_id = st.selectbox("Select Individual ID", individual_ids)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Fetch Data"):
            fetched_data = fetch_data(f"{selected_table}/{selected_id}")
            if fetched_data:
                st.json(fetched_data)
            else:
                st.warning(f"No data found for Individual ID {selected_id}")

    # Add New Record
    st.subheader(f"Add New {selected_table.capitalize()} Record")
    with st.form(f"Add {selected_table}"):
        add_form_data = {}
        table_schema = {
            "individuals": ["age", "fnlwgt", "sex", "hours_per_week", "native_country"],
            "jobdetails": ["workclass", "occupation"],
            "educationdetails": ["education_level", "education_num"],
            "incomedetails": ["income_class"],
            "relationshipdetails": ["relationship_status", "marital_status"],
        }

        for col in table_schema[selected_table]:
            if col == "workclass":
                add_form_data[col] = st.selectbox(col.capitalize(), WORKCLASS_OPTIONS)
            elif col == "marital_status":
                add_form_data[col] = st.selectbox(col.capitalize(), MARITAL_STATUS_OPTIONS)
            elif col == "education_level":
                add_form_data[col] = st.selectbox(col.capitalize(), EDUCATION_OPTIONS)
            elif col == "relationship_status":
                add_form_data[col] = st.selectbox(col.capitalize(), RELATIONSHIP_OPTIONS)
            else:
                add_form_data[col] = st.text_input(col.capitalize())

        # Automatically assign individual_id for non-individuals table
        if selected_table != "individuals":
            if individual_ids:
                add_form_data["individual_id"] = max(individual_ids) + 1
            else:
                add_form_data["individual_id"] = 1

        submit_add = st.form_submit_button("Add Record")
        if submit_add:
            response = requests.post(f"http://127.0.0.1:8000/{selected_table}/", json=add_form_data)
            if response.status_code == 200:
                st.success(f"Record added to {selected_table.capitalize()}!")
            else:
                st.error(f"Failed to add record: {response.text}")

    # Update Existing Record
    st.subheader(f"Update Existing {selected_table.capitalize()} Record")
    with st.form(f"Update {selected_table}"):
        update_record_id = st.selectbox("Select Individual ID to Update", individual_ids)
        update_form_data = {}
        for col in table_schema[selected_table]:
            update_form_data[col] = st.text_input(f"Update {col}")
        submit_update = st.form_submit_button("Update Record")
        if submit_update:
            update_form_data["individual_id"] = update_record_id
            response = requests.put(f"http://127.0.0.1:8000/{selected_table}/{update_record_id}", json=update_form_data)
            if response.status_code == 200:
                st.success(f"Record updated in {selected_table.capitalize()}!")
                st.session_state.data_updated = True
            else:
                st.error(f"Failed to update record: {response.text}")

    if "data_updated" not in st.session_state:
        st.session_state.data_updated = False

    # Fetch updated data when needed
    if st.session_state.data_updated:
        combined_data = fetch_combined_data(0, 5000)
        st.session_state.data_updated = False  # Reset after fetch

    # Delete Record
    if selected_table != "individuals":
        st.subheader(f"Delete {selected_table.capitalize()} Record")
        selected_id_to_delete = st.selectbox("Select Individual ID to Delete", individual_ids)
        if st.button("Delete Record"):
            delete_data(f"{selected_table}/{selected_id_to_delete}")

# Data Analysis Section
elif menu == "Data Analysis":
    st.title("Data Analysis")

    def execute_query(query, params=None):
        try:
            with SessionLocal() as db:
                result = db.execute(text(query), params or {})
                return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return pd.DataFrame()

    # Age Distribution
    st.subheader("Age Distribution")
    age_query = "SELECT age FROM individuals"
    age_data = execute_query(age_query)
    if not age_data.empty:
        fig_age = px.histogram(age_data, x='age', nbins=20, title="Age Distribution")
        st.plotly_chart(fig_age)
    else:
        st.warning("No data available for Age Distribution.")

    # Income Class Proportion
    st.subheader("Income Class Proportion")
    income_query = """
        SELECT income_class, COUNT(*) as count
        FROM incomedetails
        GROUP BY income_class
    """
    income_data = execute_query(income_query)
    if not income_data.empty:
        fig_income = px.pie(
            names=income_data['income_class'],
            values=income_data['count'],
            title="Income Class Distribution"
        )
        st.plotly_chart(fig_income)
    else:
        st.warning("No data available for Income Class Proportion.")

    # Average Hours Worked Per Week by Income Class
    st.subheader("Average Hours Worked Per Week by Income Class")
    hours_query = """
        SELECT income_class, AVG(hours_per_week) as avg_hours
        FROM individuals
        INNER JOIN incomedetails ON individuals.individual_id = incomedetails.individual_id
        GROUP BY income_class
    """
    hours_data = execute_query(hours_query)
    if not hours_data.empty:
        fig_hours = px.bar(
            hours_data,
            x="income_class",
            y="avg_hours",
            title="Average Hours Worked per Week",
            labels={"avg_hours": "Average Hours"}
        )
        st.plotly_chart(fig_hours)
    else:
        st.warning("No data available for Hours Worked Analysis.")

    # Workclass Distribution
    st.subheader("Workclass Distribution")
    workclass_query = """
        SELECT workclass, COUNT(*) as count
        FROM jobdetails
        GROUP BY workclass
    """
    workclass_data = execute_query(workclass_query)
    if not workclass_data.empty:
        fig_workclass = px.bar(
            x=workclass_data['workclass'],
            y=workclass_data['count'],
            title="Workclass Distribution",
            labels={"x": "Workclass", "y": "Count"}
        )
        st.plotly_chart(fig_workclass)
    else:
        st.warning("No data available for Workclass Distribution.")

    # Education Level vs Income Class
    st.subheader("Education Level vs Income Class")
    edu_income_query = """
        SELECT education_level, income_class, COUNT(*) as count
        FROM educationdetails
        INNER JOIN incomedetails ON educationdetails.individual_id = incomedetails.individual_id
        GROUP BY education_level, income_class
    """
    edu_income_data = execute_query(edu_income_query)
    if not edu_income_data.empty:
        fig_edu_income = px.bar(
            edu_income_data,
            x="education_level",
            y="count",
            color="income_class",
            title="Education Level vs Income Class",
            labels={"count": "Count", "education_level": "Education Level"}
        )
        st.plotly_chart(fig_edu_income)
    else:
        st.warning("No data available for Education vs Income Analysis.")
