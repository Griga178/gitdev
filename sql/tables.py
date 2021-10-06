import sqlite3

companies_table = '''CREATE TABLE companies (
                            id integer primary key,
                            inn text not null,
                            full_name text not null,
                            short_name,
                            adress text,
                            phone text,
                            dir_name text
                            )'''

companies_form_table = '''CREATE TABLE companies_form (
                            id integer primary key,
                            short_form text not null,
                            full_form text not null
                            )'''




con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute(companies_table)
cur.execute(companies_form_table)

for list in forms_list:
    cur.execute(f'''INSERT INTO companies_form
                    (short_form, full_form)
                    VALUES ("{list[0]}", "{list[1]}" );''')


con.commit()

user_select_0 = '''select * from companies_form'''

for row in cur.execute(user_select_0):
        print(row)

con.close()
