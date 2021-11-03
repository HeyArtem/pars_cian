import requests
import os
from bs4 import BeautifulSoup
import time
import random
import csv
import json
from datetime import datetime

"""
Собираю данные с сайта циан (недвижимость, в моей работе, в Москве)
https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=52&region=1
Интерсен способ поиска пагинации
"""

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'accept': '*/*',
    'cookie': 'CIAN_GK=08857516-1e18-434f-924b-f2d4de90af37; _gcl_au=1.1.1466831629.1635626524; uxfb_usertype=searcher; uxs_uid=d77fefc0-39c1-11ec-94a3-a5c103393aa7; tmr_lvid=d1ab2419c2f23bb2c26bc5141cf0b537; tmr_lvidTS=1635626524952; _ga=GA1.2.696366858.1635626525; afUserId=e7544069-04ff-4cd8-b86a-9d2549730c7e-p; AF_SYNC=1635626526126; serp_registration_trigger_popup=1; _ym_uid=16356297651044223474; _ym_d=1635629765; serp_stalker_banner=1; cookie_agreement_accepted=true; sopr_utm=%7B%22utm_source%22%3A+%22%22%2C+%22utm_medium%22%3A+%22referral%22%7D; _gid=GA1.2.1903476959.1635801753; session_main_town_region_id=1; session_region_id=1; __cf_bm=tolkgCPJyZixnTOdP11lZf8KIthpxz.OZCMIzTqoE6I-1635840390-0-AQqSUUAu2hp9SikkapKqT3BN0ALGit2ntOXhAGW+gvHiSuXe0OuwDVAcmUtwcovKnt4pmPUG2WELIuiDLecgO3M=; adb=1; login_mro_popup=meow; first_visit_time=1635840393467; sopr_session=9d5d7d03f10c4722; fingerprint=4d34530fe65f0a4140d9b9dbe1a23968; cto_bundle=OoNwHF9FY1JqMlkxUHRHbVkwNExlZHAlMkJ6c1NzenFmSkN1QXI1M0xQcWxTM1FIdmYyS0dFellrTXl3TU5pcVowRXRNdXVoeklETkpFM1ZwM0hCRWR1eXJhUVlFVU5XZWgzZ1RPcCUyQlowa1YyWTRSSkQyZjRFRUpMek8yUWxaOTglMkZyeVFSQzkzYWJpZmk4NzZuTVpETjZoQVVlJTJCUSUzRCUzRA; tmr_reqNum=270'
}


def get_data():
 
    # открываю ссесию
    s = requests.Session()  
    url = 'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=2&region=1'
    r = s.get(url=url, headers=headers)
    
    # проверяю и создаю директорию для сохраниния
    if not os.path.exists('data_cian'):
        os.mkdir('data_cian')
    
    # сохраняю страницу
    with open('data_cian/index_page.html', 'w') as file:
        file.write(r.text)
    
    # читаю сохраненную страницу
    with open('data_cian/index_page.html') as file:
        src = file.read()
    
    # создаю объект супа
    soup = BeautifulSoup(src, 'lxml')
    
    # предпоследний пункт в строке пагинации (это всегда номер старницы)  
    pagination_blog_penultimate = int((soup.find('div', class_='_93444fe79c--wrapper--2B3If').find_all('li')[-2]).text)
    
    # последний пункт в строке с пагинацией, на всех страницах, кроме последней это '..'. За это цепляюсь
    pagination_blog_last = (soup.find('div', class_='_93444fe79c--wrapper--2B3If').find_all('li')[-1]).text
    
    """
    Пока [-1] элемент в строке с пагинацией == '..'
    код, прибавляет единицу к [-2] элементу и открывает номер этой страницы
    У последней страницы [-1] элемент это число, это и будет номер последней страницы
    """
    
    # !для мониторинга прогресса во время выполнения
    print('Начал поиск последней стницы')
    
    while pagination_blog_last == '..':       
        url = f'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={pagination_blog_penultimate + 1}&region=1'
        
        # пауза перед запросом САЙТ ЛЕГКО ОТПРАВЛЯЕТ В КАПЧУ
        time.sleep(random.randrange(2, 5)) 
        r = s.get(url=url, headers=headers)       
        
        soup = BeautifulSoup(r.text, 'lxml')
        
        # предпоследняя цифра в строке с пагинацией
        pagination_blog_penultimate = int((soup.find('div', class_='_93444fe79c--wrapper--2B3If').find_all('li')[-2]).text)       
        
        # последняя цифра в строке с пагинацией
        pagination_blog_last = (soup.find('div', class_='_93444fe79c--wrapper--2B3If').find_all('li')[-1]).text        
    
    # когда последний элемент число 
    else:        
        last_page = int(pagination_blog_last)
         
    
        # !для мониторинга прогресса во время выполнения
        print('Последняя страница найдена')
  
    # переменная для сохранения json файла
    all_data_cards = []
    
    # шаблон для записи в csv фаил
    with open('data_cian/all_data_cards.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Наименование',
                'Комнатность',
                'Стоимость',
                'Ссылка'
            )
        )
    
    # !для мониторинга прогресса во время выполнения
    print('Стапрт этап запрос к страницам, обработка карточек')
    
    # составляю рабочие ссылки от первой до последней страницы
    for pagination_page_count in range (1, last_page + 1):
        pagination_url = f'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={pagination_page_count}&region=1'
        # print(pagination_url)
    
        # # делаю запрос к каждой странице, через паузу    
        # time.sleep(random.randrange(2, 5))
        r = s.get(url=pagination_url, headers=headers)
        
        # сохраняю каждую страницу, в имя подставляю ее номер
        with open(f'data_cian/{pagination_page_count}_pagination_page.html', 'w') as file:
            file.write(r.text)
            
        # читаю каждую страницу
        with open(f'data_cian/{pagination_page_count}_pagination_page.html') as file:
        # with open(f'data_cian/1_pagination_page.html') as file:
            src = file.read()
            
        # нахожу общий блок с карточками
        soup = BeautifulSoup(src, 'lxml')
        block_cards = soup.find('div', class_='_93444fe79c--wrapper--E9jWb').find_all('article', class_='_93444fe79c--container--2pFUD _93444fe79c--cont--1Ddh2')
        
        for card in block_cards:
            
            # наименование объкта
            try:
                card_name = card.find('div', class_="_93444fe79c--container--JdWD4").find('span', class_='').text
            except Exception as ex:
                card_name = None
            
            #  количество комнат
            try:
                card_roominess = card.find('div', class_='_93444fe79c--subtitle--iGb0_').find('span').text.replace('\n', '').replace('    ', '')
            except Exception as ex:
                card_roominess = None
                
            # стоимость
            try:
                card_price = card.find('div', class_='_93444fe79c--general--2SDGY').find('span', class_='_93444fe79c--color_black_100--A_xYw _93444fe79c--lineHeight_28px--3QLml _93444fe79c--fontWeight_bold--t3Ars _93444fe79c--fontSize_22px--3UVPd _93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER _93444fe79c--text_letterSpacing__normal--2Y-Ky').text.replace(' ', '').replace('₽', '')
            except Exception as ex:
                card_price = None
            
            # ссылка на карточку
            try:
                card_link = card.find('div', class_='_93444fe79c--general--2SDGY').find('a').get('href')
            except Exception as ex:
                card_link = None
            
            # записываю данные в csv
            with open('data_cian/all_data_cards.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        card_name,
                        card_roominess,
                        card_price,
                        card_link
                    )
                )
                
            # упаковываю данные в переменную, для дальнейшей записи в json
            all_data_cards.append(
                {
                    'card_name': card_name,
                    'card_roominess': card_roominess,
                    'card_price': card_price,
                    'card_link': card_link
                }
            )
            
            # print(f'Наименование: {card_name}\nКомнатность: {card_roominess}\nСтоимость: {card_price}\nСсылка на карточку: {card_link}\n-*-*-*-*-*-*-*\n')
        
        # пауза после каждой страницы
        print('пауза после каждой страницы')
        time.sleep(random.randrange(4, 9))
            
        # монитор прогресса
        print(f'[info] бработана {pagination_page_count} страница из {last_page} страниц')
        
    # упакованные в переменную данные, запишу в json
    with open('data_cian/all_data_cards.json', 'a') as file:
        json.dump(all_data_cards, file, indent=4, ensure_ascii=False)


def main():
    # время старта кода
    time_start = time.time()
    print(f'Время старта кода: {datetime.fromtimestamp(time_start)}\n')
    
    # активация функции сбора инфы
    get_data()
    
    # время окончания работы кода
    time_finish = time.time()
    
    # общее время работы кода
    time_total = time_finish - time_start
    
    # итоговая инфа о времени работы кода
    print(f'* * * \n[info]: Время старта кода: {datetime.fromtimestamp(time_start)}\nВремя окончания работы кода: {datetime.fromtimestamp(time_finish)}\nВремя работы кода: {time_total/60} мин.')
    
    
if __name__ == '__main__':
    main()
