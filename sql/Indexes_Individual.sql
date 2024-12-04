SELECT *
FROM Individuals i
JOIN IncomeDetails incd ON i.individual_id = incd.individual_id
WHERE incd.income_class = '>50K';


-- Use only required columns
EXPLAIN ANALYZE
SELECT i.individual_id, i.age, incd.income_class
FROM Individuals i
JOIN IncomeDetails incd ON i.individual_id = incd.individual_id
WHERE incd.income_class = '>50K';




