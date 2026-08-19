
q1 = '''
select * from employees AS e
join departments as d on e.department_id = d.id;
'''
q2 = '''
SELECT e.name as Emp_name, d.name as dep_name, p.name as proj_name
FROM employees AS e
LEFT JOIN departments AS d ON e.department_id = d.id
LEFT JOIN employees_projects AS e_p ON e.id = e_p.employee_id
LEFT JOIN projects AS p ON e_p.project_id = p.id;
'''
q3 = '''
SELECT * FROM departments
JOIN projects ON departments.id = projects.department_id
'''
