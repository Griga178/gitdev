'''
    Копируем столбец name в upprName + uppercase
'''
from database import Data_base_API
from database.tables import Product

DB_API = Data_base_API()
query = DB_API.products.session.query(Product).all()

print(len(query))

i = 0
j = 0
for row in query:
    j += 1
    # if not row.search_name.isupper():
    if not row.search_name:

        # print(j)
        # print()
        row.search_name = row.name.upper()
        DB_API.products.session.add(row)
        print('change', i, row.search_name)
        i+=1
    else:
        print("True", j, end = '\r')
    if j % 1000 == 0:
        DB_API.products.session.commit()
DB_API.products.session.commit()
print("save", i, end = '\r')
print()
print( j)
