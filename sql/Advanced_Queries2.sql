SELECT 
    jd.occupation,
    COUNT(i.individual_id) AS high_earners_count
FROM individuals i
LEFT JOIN jobdetails jd ON i.individual_id = jd.individual_id
LEFT JOIN incomedetails inc ON i.individual_id = inc.individual_id
WHERE inc.income_class = '>50K'
GROUP BY jd.occupation
ORDER BY high_earners_count DESC
LIMIT 5;
