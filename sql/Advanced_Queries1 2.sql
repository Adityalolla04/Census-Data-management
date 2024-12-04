SELECT 
            i.individual_id, i.age, i.sex, i.fnlwgt, i.hours_per_week, i.native_country, 
            jd.workclass, jd.occupation, 
            ed.education_level, ed.education_num,
            inc.income_class, 
            rel.relationship_status, rel.marital_status
        FROM individuals i
        LEFT JOIN jobdetails jd ON i.individual_id = jd.individual_id
        LEFT JOIN educationdetails ed ON i.individual_id = ed.individual_id
        LEFT JOIN incomedetails inc ON i.individual_id = inc.individual_id
        LEFT JOIN relationshipdetails rel ON i.individual_id = rel.individual_id
        WHERE inc.income_class = '>50K'
        ORDER BY individual_id
       