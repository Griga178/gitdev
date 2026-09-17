-- 1 Выведи для каждого пользователя первое наименование, которое он заказал (первое по времени транзакции).
Transactions.transaction_ts
Transactions.user_id
Transactions.transaction_id
Transactions.item

SELECT DISTINCT
    user_id,
    FIRST_VALUE(item) OVER(PARTITION BY user_id ORDER BY transaction_ts) AS item
FROM Transactions;

-- 2. Последний арендатор комнаты

WITH Last_reserv AS (
SELECT
    room_id,
    MAX(end_date) AS end_date
FROM Reservations
group by room_id
)
select
    res.room_id as room_id,
    u.name as name,
    res.end_date as end_date

from Reservations as res
JOIN Last_reserv AS lr
JOIN Users as u ON u.id = res.user_id
where res.room_id = lr.room_id and res.end_date = lr.end_date;

-- 3. Процент активных пользователей
SELECT
    ROUND((SELECT count(*) FROM (
        -- ID СНИМАВШИХ
        SELECT user_id FROM Reservations
        UNION
        -- ID СДАВАВШИХ
        SELECT Rooms.owner_id as room_owner_user_id
        FROM Reservations as res JOIN Rooms on res.room_id = Rooms.id) AS usfull)
    /
    (SELECT COUNT(*) FROM USERS) * 100,2) AS percent


-- 4. delete
WITH TEMP_TBL AS (SELECT MIN(id) AS min_in FROM Person GROUP BY email)
DELETE FROM Person WHERE id NOT IN (SELECT min_id FROM TEMP_TBL);

-- 5. Last Person to Fit in the Bus
WITH calc_tbl AS (SELECT *, SUM(Weight) OVER(ORDER BY turn ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS Total_Weight
FROM Queue
ORDER BY turn DESC)
SELECT person_name FROM calc_tbl
WHERE Total_Weight <= 1000
LIMIT 1;

-- Не менее трех значений подряд
WITH calc_tbl AS (
  SELECT
  ID,
  Num,
  LAG(Num, 1) OVER(ORDER BY ID) as sec_num,
  LAG(Num, 2) OVER(ORDER BY ID) as third_num
FROM Logs
)
SELECT DISTINCT num  as ConsecutiveNums FROM calc_tbl
WHERE num = sec_num AND num = third_num
ORDER BY num DESC

-- Найти ID с самым большим количеством заказов по годам
WITH year_parts AS (
  SELECT
    EXTRACT(YEAR FROM ord_datetime) as year,
    ord_an
  FROM Orders
)
SELECT DISTINCT
  ord.year as year,
  an.an_id as an_id,
  COUNT(*) OVER(PARTITION BY ord.year, an.an_id) as cnt
FROM year_parts as ord
JOIN Analysis as an ON ord.ord_an = an.an_id
ORDER BY year, an_id;
-- II ВАРИАНТ
SELECT
    EXTRACT(YEAR FROM ord_datetime) AS year,
    an.an_id,
    COUNT(*) AS cnt
FROM Orders AS ord
JOIN Analysis AS an ON ord.ord_an = an.an_id
GROUP BY year, an.an_id
ORDER BY year, an.an_id;


-- 8
8. Представьте, что у вас в базе данных есть две таблицы: TABLE1 и TABLE2. Ниже будут приведены несколько SQL-запросов.
Нужно ответить на один простой вопрос: отработает ли данный запрос или упадет с ошибкой? И объяснить, почему.
8.1 select * from TABLE1 group by ID
  Ошибка: будут задеты столбцы, не учавствующие в группировке

8.2 select field1 from TABLE1 group by field1, field2
  Отработает, при условии, что в TABLE1 есть столбцы field1, field2

8.3 select field1, field2 from TABLE1 group by field1, field2 having field2 = 0
(Примечание: field1, field2 являются числовыми полями)
  Отработает: отфильтрует результат group by

8.4 update TABLE1 set field1 = row_number() from TABLE1
  Ошибка: неверный синтаксис, оконная функция не выполнится

8.5 insert into TABLE1 (field1, field2, field3) values ('1','2')
(Примечание: field1, field2, field3 являются текстовыми полями)
  Ошибка: передано 2 аргумента, когда указано 3

8.6 delete from TABLE1 having count(field1) > 1
  Ошибка: нарушен синтаксис having используетя только для select

8.7 truncate TABLE1
  Отработает

8.8 select * from table1 as t inner join table2 as tt on 1 = tt.field1
  Отработает, для каждой строки где tt.field1 = 1 притянет все строки table1

8.9 select id,sum(value) over(partition by i order by y), * from table1
(Примечание: все поля существуют в таблице и соответствуют нужному типу данных)
  Отработает, вернет две колонки "id"

8.10 select count(*) from table1 ,table2
  Отработает, вернет количество строк table1*table2

8.11 select * from table1 where null = null or null <> null or 123 <> null or null is null
(Примечание: представьте, что таблица table1 не пустая. Вернет ли этот запрос строки? Почему?)
  Отработает, вернет все строки, так null is null
