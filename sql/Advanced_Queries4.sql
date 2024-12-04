SELECT 
    ed.education_level,
    COUNT(CASE WHEN inc.income_class = '>50K' THEN 1 END) * 100.0 / COUNT(*) AS high_earner_percentage
FROM individuals i
LEFT JOIN educationdetails ed ON i.individual_id = ed.individual_id
LEFT JOIN incomedetails inc ON i.individual_id = inc.individual_id
GROUP BY ed.education_level
ORDER BY high_earner_percentage DESC;
