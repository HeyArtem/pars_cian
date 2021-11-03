import time
from datetime import datetime

# a = 1

# while a < 5:
#     print('Цикл выполнился', a, 'раз')
#     a += 1
# print('Цикл окончен')

# a = 1
# while a == 1:
#     b = input('Как тебя зовут?')
#     print(f'Привет {b} , Добро пожаловать!')

# a = 1
# while a < 10:
#     print(f'is good, a={a}')
#     a += 1
# else:
#     print(f'No good! a={a}')

# a = 1
# while a < 5:
#     a += 1
    
#     if a == 3:
#         break
#     print(a)

# a = 1
# while a < 5:
#     a += 1
    
#     if a == 3:
#         continue
#     print(a)
    
 # время старта кода
# time_start = time.time()
# time_start_r = round(time_start, 2)
# time_start_r_n = datetime.fromtimestamp(time_start_r)
# # time_start_r_n1111 = round(time_start_r_n, 2)
# # print(time_start)
# # print(time_start_r)
# print(time_start_r_n)
# # print(time_start_r_n1111)
# # print(f'Время старта кода: {datetime.fromtimestamp(time_start_r)}\n')

from bs4 import BeautifulSoup


with open("/home/heyartem/PycharmProjects/Parsing_project/cian/data_cian/1_pagination_page.html") as file:
    src = file.read()
    
soup = BeautifulSoup(src, "lxml")

prices = soup.find_all("span", attrs={"data-mark": "MainPrice"})

for price in prices:
    print(price.text)
