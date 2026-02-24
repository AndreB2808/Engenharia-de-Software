DESC DEPARTMENTS;

DESC EMPLOYEES;
SELECT 
    employee_ID,
    last_name,
    job_id,
    commission_pct,
    phone_number,
    hire_date AS STARTDATE
FROM EMPLOYEES;

SELECT DISTINCT job_id FROM EMPLOYEES;

SELECT 
    employee_ID "Emp #",
    last_name "Employee",
    job_id "Job",
    hire_date "Hire Date"
FROM EMPLOYEES;

SELECT last_name||', '||job_id "Employee and Title" FROM EMPLOYEES;

