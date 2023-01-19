import os
import itertools
# from datetime import datetime as dt

# print(dt.strptime(str(dt.now()),"%Y-%m-%d %H:%M:%S.%f"))

# fp = open('Aman.txt', 'r+')
# # fp.seek(0)
# last_read = int(fp.readline())
# print(last_read)
# i=0
# # print("LA ",last_read)
# for m in fp.readlines():
#     if i>=last_read:
#         print("Aman> "+m)
#     i+=1

# fp.seek(0)
# fp.write(str(i))

# fp.close()
# print(type(os.stat(os.path.join("2201_inbox", "Aman.txt")).st_mtime))

# g = (1,2)
# g[1] = 3
# print(g)

import traceback

try:
    a = 100/0
    print(a)
except Exception as e:
    print(e)