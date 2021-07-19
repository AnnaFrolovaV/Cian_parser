# Программа парсит сайт Циана, после чего достает данные о каждой квартире размещенной там
# Данные сохраняются в таблице 
# После чего можно найти все квартиры с определнными характеристиками (станция метро, количество комнат и т.д.)

import requests
import urllib.request
from tqdm.notebook import tqdm
import six
import requests
from bs4 import BeautifulSoup
import pandas as pd

titles = []
residential_complexes = []
metro = []
remotnesses = []
cities = []
districts = []
regions = []
streets = []
house_nums = []
fullprices = []
prices_m2 = []
links = []

for p in range(1, 100):
    page_num = p
    for r in range(1, 3):
        region = r
        offer_type = 'flat'
        url = f'https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type={offer_type}&p={page_num}&region={region}'
        try:
            response = requests.get(url)
        except:
            break
        soup = BeautifulSoup(response.content, 'html.parser')
        for advert_html_block in soup.find_all('div', '_93444fe79c--content--2IC7j'):
            #advert_html_block = soup.find_all('div', '_93444fe79c--content--2IC7j')[i]
            # кол-во комнат + тип жилья + площадь + этаж
            advert_title = advert_html_block.find_all('div', '_93444fe79c--container--JdWD4')[0].span.span.text
            if (advert_html_block.find_all('div', '_93444fe79c--subtitle--iGb0_') != []):
                advert_title = advert_html_block.find_all('div', '_93444fe79c--subtitle--iGb0_')[0].span.text
            # жилой комплекс
            try:
                advert_residential_complex = advert_html_block.find_all('div', '_93444fe79c--container--2h0AF')[0].div.a.text
            except:
                advert_residential_complex = ''
            # метро
            if (advert_html_block.find_all('a', '_93444fe79c--link--3ruIo') != []):
                advert_metro = advert_html_block.find_all('a', '_93444fe79c--link--3ruIo')[0].text
            else:
                advert_metro = ''
            # сколько минут от метро
            if (advert_html_block.find_all('div', '_93444fe79c--remoteness--1BnAC') != []):
                advert_remoteness = advert_html_block.find_all('div', '_93444fe79c--remoteness--1BnAC')[0].text
            else:
                advert_remoteness = ''
            # город
            try:
                advert_city = advert_html_block.find_all('a', '_93444fe79c--link--10mjQ')[0].text
            except:
                advert_city = ''
            # административный округ
            try:
                advert_district = advert_html_block.find_all('a', '_93444fe79c--link--10mjQ')[1].text
            except:
                advert_district = ''
            # район
            try:
                advert_region = advert_html_block.find_all('a', '_93444fe79c--link--10mjQ')[2].text
            except:
                advert_region = ''
            # улица
            try:
                advert_street = advert_html_block.find_all('a', '_93444fe79c--link--10mjQ')[4].text
            except:
                advert_street = ''
            # номер дома
            try:
                 advert_hmun = advert_html_block.find_all('a', '_93444fe79c--link--10mjQ')[5].text
            except:
                advert_hnum = ''
            prices = advert_html_block.find_all('div', '_93444fe79c--container--2h0AF _93444fe79c--container-l--5Wrcc')[1]
            # полная цена
            advert_fullprice = prices.find_all('span', '_93444fe79c--color_black_100--A_xYw _93444fe79c--lineHeight_28px--3QLml _93444fe79c--fontWeight_bold--t3Ars _93444fe79c--fontSize_22px--3UVPd _93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER')[0].text
            # цена на квадратный метр
            advert_price_m2 = prices.find_all('p', '_93444fe79c--color_gray60_100--3VLtJ _93444fe79c--lineHeight_20px--2dV2a _93444fe79c--fontWeight_normal--2G6_P _93444fe79c--fontSize_14px--10R7l _93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER')[0].text
            # ссылки
            try:
                advert_link = advert_html_block.find_all('a', '_93444fe79c--link--39cNw')[0]['href']
            except:
                advert_link = ''

            titles.append(advert_title)
            residential_complexes.append(advert_residential_complex)
            metro.append(advert_metro)
            remotnesses.append(advert_remoteness)
            cities.append(advert_city)
            districts.append(advert_district)
            regions.append(advert_region)
            streets.append(advert_street)
            house_nums.append(advert_hmun)
            fullprices.append(advert_fullprice)
            prices_m2.append(advert_price_m2)
            links.append(advert_link)
            #print(advert_title, '/', advert_residential_complex, '/', advert_metro, '/', advert_remoteness, '/', advert_city, '/', advert_district)

import pandas as pd

df = pd.DataFrame(
    {
        'Title': titles,
        'Residential complex': residential_complexes,
        'Nearest metro': metro,
        'Remotnesses': remotnesses,
        'City': cities,
        'District': districts,
        'Region': regions,
        'Street': streets,
        'House num': house_nums,
        'Full price': fullprices,
        'Price for m2' : prices_m2,
        'Link': links
    }
)
#df.drop_duplicates(subset=['meal_urls'], inplace=True)
df

city = 'Москва'
metro = 'Китай-город'
rooms = '3-'
indexes_match_queries = df.apply(
        lambda row: str(city).lower() in str(row['City']).lower(),
        axis=1,
    )
df1 = df[indexes_match_queries]
indexes_match_queries1 = df1.apply(
    lambda row: str(metro).lower() in str(row['Nearest metro']).lower(),
    axis=1,
)
df2 = df1[indexes_match_queries1]
indexes_match_queries1 = df2.apply(
    lambda row: str(rooms).lower() in str(row['Title']).lower(),
    axis=1,
)
df3 = df2[indexes_match_queries1]
print(str(df3.sample(1)['Link']))
