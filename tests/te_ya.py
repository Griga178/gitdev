tpath = 'C:/Users/G.Tishchenko/Desktop/1t.txt'

with open(tpath, "r+", encoding = 'utf8') as stream:
    a = stream.read()
    print([a])
    # counter = 0
    # for line in stream:
    #     counter += 1
    #     print([line], end = ' - ')
    #     # line = line.upper()
    #     # line = line.lower()
    #     print([line])
    # stream.seek(0)
    # print(counter)
    # print(range(counter))
    # for row_num in range(counter):
    #     string = stream.readline()
    #     print(string)
    #     string = string.upper()
    #     stream.fileno()
    # print(dir(stream))
