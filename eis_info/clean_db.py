"""
Содержит разовые или не очень функции для очистки данных в БД
"""
import os
import duckdb

db_path = 'database/analytics.duckdb'

def clean_by_file(sql_query_path):
    with duckdb.connect(db_path) as conn:
        with open(sql_query_path, 'r', encoding='utf-8') as f:
            query = f.read()
            resp = conn.execute(query)
            return resp.fetchall()

def clean_by_query(query):
    with duckdb.connect(db_path) as conn:
        resp = conn.execute(query)
        return resp.fetchall()

if __name__ == "__main__":

    # оставляет только цифры в eis_id
    clean_func_1 = 'sql/clean_consumer_eis_id.sql'
    # rsps = clean_by_file(clean_func_1)

    query2 = """
        SELECT eis_id
        FROM consumers
        WHERE eis_id IS NOT NULL
            AND regexp_matches(eis_id, '[^0-9]')
        """
    query3 = """
        SELECT eis_id
        FROM consumers
        WHERE eis_id IS NULL
    """

    query4 = """
        SELECT
            pd.date,
            pd.card_parsed AS registered,
            COALESCE(oc.cnt, 0) AS actual,
            pd.card_parsed - COALESCE(oc.cnt, 0) AS diff
        FROM parser_data pd
        LEFT JOIN (
            SELECT placement_date, COUNT(*) AS cnt
            FROM order_cards
            GROUP BY placement_date
        ) oc ON pd.date = oc.placement_date
        WHERE pd.is_parsed = TRUE
          AND pd.card_parsed != COALESCE(oc.cnt, 0);
    """
    rsps = clean_by_query(query4)
    cnt = 0
    for i in rsps:
        cnt += 1
        print(cnt, i)
        # if len(i[0]) > 9:
        #     print(cnt, i)
    print("Кол-во строк:", len(rsps))
