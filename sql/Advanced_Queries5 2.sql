SELECT 
    i.sex,
    COUNT(i.individual_id) AS count_high_earners,
    COUNT(i.individual_id) * 100.0 / (SELECT COUNT(*) FROM incomedetails WHERE income_class = '>50K') AS percentage
FROM individuals i
LEFT JOIN incomedetails inc ON i.individual_id = inc.individual_id
WHERE inc.income_class = '>50K'
GROUP BY i.sex
ORDER BY percentage DESC;
