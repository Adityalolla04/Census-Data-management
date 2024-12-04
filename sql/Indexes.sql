-- Indexes to optimize filtering and joining
CREATE INDEX idx_jobdetails_id ON JobDetails(individual_id);
CREATE INDEX idx_incomedetails_id ON IncomeDetails(individual_id);
CREATE INDEX idx_incomedetails_income_class ON IncomeDetails(income_class);
CREATE INDEX idx_jobdetails_occupation ON JobDetails(occupation);

EXPLAIN ANALYZE 
SELECT jd.occupation,
       COUNT(i.individual_id) AS high_earner_count
FROM Individuals i
JOIN JobDetails jd ON i.individual_id = jd.individual_id
JOIN IncomeDetails inc ON i.individual_id = inc.individual_id
WHERE inc.income_class = '>50K'
GROUP BY jd.occupation
ORDER BY high_earner_count DESC
LIMIT 5;

