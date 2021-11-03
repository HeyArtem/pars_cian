"""
Попробовал собрать данные с сайта cian. Нужно делать большие паузы, т.к. отправляет в капчу.
Время старта, окончания, итоговая продолжительность

Особенности:
-поиск последней страницы в пагинации
-поиск стоимости (в test.py)
prices = soup.find_all("span", attrs={"data-mark": "MainPrice"})
из:
<span data-mark="MainPrice" class="_93444fe79c--color_black_100--A_xYw _93444fe79c--lineHeight_28px--3QLml _93444fe79c--fontWeight_bold--t3Ars _93444fe79c--fontSize_22px--3UVPd _93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER _93444fe79c--text_letterSpacing__normal--2Y-Ky"></span>
<span class="">9 828 505&nbsp;₽</span>
"""