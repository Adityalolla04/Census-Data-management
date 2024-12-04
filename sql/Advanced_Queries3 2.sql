SELECT 
    jd.workclass,
    inc.income_class,
    AVG(i.hours_per_week) AS avg_hours_worked
FROM individuals i
LEFT JOIN jobdetails jd ON i.individual_id = jd.individual_id
LEFT JOIN incomedetails inc ON i.individual_id = inc.individual_id
GROUP BY jd.workclass, inc.income_class
ORDER BY jd.workclass, inc.income_class;
