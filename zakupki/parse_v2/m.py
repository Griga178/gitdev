from main import Parser_ver_2, get_contract_amount

p = Parser_ver_2()

response = p.get_query()
# print(get_contract_amount(response))

f = '30.11.2023'
t = '12.02.2024'

p.set_dates(date_from = f, date_to = t)

# print(p.date_from)
# print(p.date_to)

p.parse_contract_numbers()
