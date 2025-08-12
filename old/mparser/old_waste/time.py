from datetime import datetime as tt

time = tt.now()

list_time = ['2022-12-27 00:46:17.74876',
            '2022-12-27 00:46:17.574876',
            '2022-12-27 00:46:17.574876',
            '2022-12-27 00:46:17.574875']
# print(time)
new_list = []
for te in list_time:
    argg = tt.strptime(te, '%Y-%m-%d %H:%M:%S.%f')
    # print(argg)
    new_list.append(argg)

f = tt.strptime('2022/11/2', '%Y/%m/%d')
max_t = min(new_list)
print(f, max_t)
