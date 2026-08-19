-- сброс для повторного запуска
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees_projects;

-- СОЗДАНИЕ ТАБЛИЦ
CREATE TABLE IF NOT EXISTS employees (
  id INTEGER PRIMARY KEY,
  name VARCHAR,
  surname VARCHAR,
  salary FLOAT,
  department_id INTEGER
);

CREATE TABLE IF NOT EXISTS departments (
  id INTEGER PRIMARY KEY,
  name VARCHAR UNIQUE
);

CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY,
  name VARCHAR UNIQUE,
  department_id INTEGER

);

CREATE TABLE IF NOT EXISTS employees_projects (
  employee_id INTEGER,
  project_id INTEGER
);

-- вставка первичных данных
INSERT INTO departments (name) VALUES
  ('Engineers'),
  ('Analysts'),
  ('Managers');

INSERT INTO employees (name, surname, salary, department_id) VALUES
  ('Veronika', 'Kuharskaya', 150000, 3),
  ('Uladzislava', 'Kuprykava', 150000, 3),

  ('Виктория', 'Аладко', 110000, 2),
  ('Андрей', 'Бордодымов', 110000, 2),
  ('Людмила', 'Визжачая', 120000, 2),
  ('Михаил', 'Денисов', 113000, 2),

  ('Дмитрий', 'Дубовой', 120000, 1),
  ('Тимофей', 'Зубарев', 119000, 1),
  ('Кирилл', 'Ильинов', 121000, 1),
  ('Анастасия', 'Кадынина', 115000, 1);

INSERT INTO projects (name, department_id) VALUES
  ('QuickPatch', (SELECT id FROM departments WHERE name = 'Engineers')),
  ('CleanSweep', (SELECT id FROM departments WHERE name = 'Engineers')),
  ('StarterFlow', (SELECT id FROM departments WHERE name = 'Engineers')),

  ('QuickLook', (SELECT id FROM departments WHERE name = 'Analysts')),
  ('DataCheck', (SELECT id FROM departments WHERE name = 'Analysts')),
  ('TrendSnap', (SELECT id FROM departments WHERE name = 'Analysts')),

  ('TaskPulse', (SELECT id FROM departments WHERE name = 'Managers')),
  ('GoalSnap', (SELECT id FROM departments WHERE name = 'Managers')),
  ('BridgeLog', (SELECT id FROM departments WHERE name = 'Managers'));

INSERT INTO employees_projects VALUES
  (1, 1),  (1, 2), (2, 2), (2, 3),
  (3, 4),  (4, 5),  (5, 6),  (6, 4),
  (7, 7),  (8, 8),  (9, 9),  (10, 7);

-- ЗАДАНИЯ
-- 1 Добавить новый проект и новый отдел, чтобы они были связаны
-- WITH new_dep_id AS (  INSERT INTO departments (name) VALUES ('Operational Reliability Unit')  RETURNING id)
-- INSERT INTO projects (name, department_id) SELECT 'LightCheck', id FROM new_dep_id;
INSERT INTO departments (name) VALUES ('Operational Reliability Unit');
INSERT INTO projects (name, department_id) SELECT 'LightCheck', (SELECT id FROM departments WHERE name = 'Operational Reliability Unit');

-- 2 Добавить туда двух новых сотрудников и по одному перевести из двух других отделов
-- Добавляем новых
WITH dep_id AS (SELECT id FROM departments WHERE name = 'Operational Reliability Unit')
INSERT INTO employees (name, surname, salary, department_id)
  SELECT 'Григорий', 'Тищенко', 110000, id FROM dep_id
  UNION
  SELECT 'Андрей', 'Петров', 120000, id FROM dep_id;
-- назначаем на новый проект
INSERT INTO employees_projects VALUES
  ((SELECT id FROM employees WHERE name = 'Григорий' AND surname = 'Тищенко'), (SELECT id FROM projects WHERE name = 'LightCheck')),
  ((SELECT id FROM employees WHERE name = 'Андрей' AND surname = 'Петров'), (SELECT id FROM projects WHERE name = 'LightCheck'));
-- Переводим старых
BEGIN;
-- меняем отдел сотрудников
WITH dep_id AS (SELECT id FROM departments WHERE name = 'Operational Reliability Unit')
UPDATE employees
SET department_id = (SELECT id FROM dep_id)
WHERE id = 3 OR id = 7;
-- меняем проекты сотрудников
-- WITH proj_id AS (
--   SELECT id
--   FROM projects
--   WHERE name = 'LightCheck' AND department_id = (SELECT id FROM departments WHERE name = 'Operational Reliability Unit'))
-- UPDATE employees_projects
-- SET project_id = proj_id.id FROM proj_id
-- WHERE employee_id IN (3, 4);
UPDATE employees_projects
SET project_id = (SELECT id FROM projects WHERE name = 'LightCheck'AND department_id = (SELECT id FROM departments WHERE name = 'Operational Reliability Unit'))
WHERE employee_id IN (3, 7);
-- если у 1 сотрудника 2 проекта, то после UPDATE 2 одинаковые связи
COMMIT;

-- 3 Увеличить зарплаты сотрудникам по названию этого отдела на 10%
UPDATE employees as e
SET salary = salary * 1.1
WHERE department_id = (SELECT id FROM departments WHERE name = 'Operational Reliability Unit');

-- 4 Найти сотрудников с самой высокой и самой низкой зарплатой в отделе
-- максимальная ЗП
WITH dep_id AS (SELECT id FROM departments WHERE name = 'Operational Reliability Unit')
SELECT *
FROM employees
WHERE department_id = (SELECT id FROM dep_id)
AND
salary = (SELECT salary FROM employees WHERE department_id = (SELECT id FROM dep_id) ORDER BY salary DESC);
-- минимальная ЗП
WITH dep_id AS (SELECT id FROM departments WHERE name = 'Operational Reliability Unit')
SELECT *
FROM employees
WHERE department_id = (SELECT id FROM dep_id)
AND
salary = (SELECT salary FROM employees WHERE department_id = (SELECT id FROM dep_id) ORDER BY salary ASC);

-- 5 Добавить таблице сотрудников столбик дата найма и заполнить значениями
ALTER TABLE employees ADD COLUMN date_hired DATE;
-- руками добавляем даты, так как неизвестна используемая БД (PostgreSQl, MySQL)
UPDATE employees SET date_hired = '2025-01-01' WHERE id = 1;
UPDATE employees SET date_hired = '2025-02-01' WHERE id = 2;
UPDATE employees SET date_hired = '2026-03-01' WHERE id = 3;
UPDATE employees SET date_hired = '2025-04-01' WHERE id = 4;

UPDATE employees SET date_hired = '2026-01-01' WHERE id = 5;
UPDATE employees SET date_hired = '2026-02-01' WHERE id = 6;
UPDATE employees SET date_hired = '2026-03-01' WHERE id = 7;
UPDATE employees SET date_hired = '2026-04-01' WHERE id = 8;

UPDATE employees SET date_hired = '2026-05-01' WHERE id = 9;
UPDATE employees SET date_hired = '2026-05-11' WHERE id = 10;
UPDATE employees SET date_hired = '2026-06-15' WHERE id = 11;
UPDATE employees SET date_hired = '2026-06-17' WHERE id = 12;

-- 6 Вывести порядок найма сотрудников внутри каждого отдела
SELECT
	d.name AS department,
	DENSE_RANK() OVER(partition by department_id ORDER BY e.date_hired) AS num,
  e.name,
  e.surname,
  e.date_hired
FROM employees AS e
JOIN departments AS d ON d.id = e.department_id
ORDER BY department;

-- 7 Найти сотрудников, которые работают дольше всех в своем отделе
-- GROUP BY + JOIN
WITH md AS (SELECT
	department_id,
	MIN(date_hired) as date
FROM employees
GROUP BY department_id)
SELECT e.name, e.date_hired, round(julianday('now') - julianday(e.date_hired)) as days_ago
FROM employees AS e
JOIN md ON e.date_hired = md.date;

-- window func + where
with older as (select
	department_id,
	name,
    date_hired,
	dense_rank() over(partition by department_id order by date_hired) as dr
from employees)
select
	d.name as dep_name,
	older.name as emp_name,
	date_hired,
  -- SQLite
	round(julianday('now') - julianday(date_hired)) as days_ago
  -- PostgreSQL
  -- round(CURRENT_DATE - date_hired) as days_ago
from older
join departments as d on older.department_id = d.id
where dr = 1;

-- 8 Найти разницу между средней зарплатой текущего и соседних отделов
with dep_avg_sal as (select
	department_id as d_id,
	avg(salary) as avg_sal
from employees
group by department_id
order by d_id asc)

select
	d.id,
	d.name,
	round(das.avg_sal) as avg_sal,
	round(lag(avg_sal) over() - avg_sal) as prev_diff,
	round(lead(avg_sal) over() - avg_sal) as next_diff
from dep_avg_sal as das
join departments as d on das.d_id = d.id;

-- 9 Определить среднее время работы сотрудников по проектам
-- *нет завершенных проектов
select
	p.name as proj_name,
	avg(round(julianday('now') - julianday(date_hired))) avg_days
from employees as e
join employees_projects as ep on e.id = ep.employee_id
join projects as p on p.id = ep.project_id
group by p.name
order by avg_days;

-- 10 Определить процент зарплаты сотрудника от общей суммы зарплат в его отделе
with dep_avg_sal as (
	select
		sum(salary) as sum_sal,
		department_id
	from employees
	group by department_id
)
select
	d.name,
	e.name,
	e.salary,
	das.sum_sal,
	round(e.salary / das.sum_sal * 100, 2) as sal_per_cent
from employees as e
join dep_avg_sal as das on e.department_id = das.department_id
join departments as d on e.department_id = d.id
order by d.name;
