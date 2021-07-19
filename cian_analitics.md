```python
# Программа парсит сайт Циана, после чего достает данные о каждой квартире размещенной там
# Данные сохраняются в таблице 
# После чего можно найти все квартиры с определнными характеристиками (станция метро, количество комнат и т.д.)
```


```python
import requests
import urllib.request
from tqdm.notebook import tqdm
import six
import requests
from bs4 import BeautifulSoup
import pandas as pd
```


```python
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
```


```python
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
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Title</th>
      <th>Residential complex</th>
      <th>Nearest metro</th>
      <th>Remotnesses</th>
      <th>City</th>
      <th>District</th>
      <th>Region</th>
      <th>Street</th>
      <th>House num</th>
      <th>Full price</th>
      <th>Price for m2</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3-комн. кв., 85,3 м², 1/6 этаж</td>
      <td>ЖК «City Park»</td>
      <td>Деловой центр</td>
      <td>10 минут пешком</td>
      <td>Москва</td>
      <td>ЦАО</td>
      <td>р-н Пресненский</td>
      <td>Мантулинская улица</td>
      <td>9к6</td>
      <td>38 500 000 ₽</td>
      <td>451 348 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/251974435/</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3-комн. апарт., 113,3 м², 5/15 этаж</td>
      <td>ЖК «Hill8»</td>
      <td>Алексеевская</td>
      <td>4 минуты пешком</td>
      <td>Москва</td>
      <td>СВАО</td>
      <td>р-н Останкинский</td>
      <td>проспект Мира</td>
      <td>вл95</td>
      <td>39 810 455 ₽</td>
      <td>351 372 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/239980039/</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3-комн. апарт., 111,9 м², 9/10 этаж</td>
      <td>ЖК «Клубный дом Maison Rouge»</td>
      <td>Менделеевская</td>
      <td>2 минуты пешком</td>
      <td>Москва</td>
      <td>ЦАО</td>
      <td>р-н Тверской</td>
      <td>улица Палиха</td>
      <td>4</td>
      <td>74 525 400 ₽</td>
      <td>666 000 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/247916427/</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3-комн. апарт., 208,7 м², 8/8 этаж</td>
      <td>ЖК «LUMIN»</td>
      <td>Китай-город</td>
      <td>2 минуты пешком</td>
      <td>Москва</td>
      <td>ЦАО</td>
      <td>р-н Таганский</td>
      <td>Славянская площадь</td>
      <td>2/5/4с5</td>
      <td>260 875 000 ₽</td>
      <td>1 250 000 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/250364689/</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3-комн. апарт., 94 м², 2/20 этаж</td>
      <td>ЖК «Клубный дом SOHO+NOHO»</td>
      <td>Савеловская</td>
      <td>10 минут пешком</td>
      <td>Москва</td>
      <td>САО</td>
      <td>р-н Беговой</td>
      <td>Бумажный проезд</td>
      <td>4</td>
      <td>35 000 000 ₽</td>
      <td>372 340 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/260414438/</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5533</th>
      <td>2-комн. кв., 59,3 м², 2/9 этаж</td>
      <td>ЖК «Кантемировская 11»</td>
      <td>Лесная</td>
      <td>8 минут пешком</td>
      <td>Санкт-Петербург</td>
      <td>р-н Выборгский</td>
      <td>Сампсониевское</td>
      <td>Кантемировская 11 ЖК</td>
      <td>к1</td>
      <td>12 085 340 ₽</td>
      <td>203 800 ₽/м²</td>
      <td>https://spb.cian.ru/sale/flat/259812416/</td>
    </tr>
    <tr>
      <th>5534</th>
      <td>1-комн. кв., 54,06 м², 18/20 этаж</td>
      <td>ЖК «Golden City»</td>
      <td>Приморская</td>
      <td>8 минут на транспорте</td>
      <td>Санкт-Петербург</td>
      <td>р-н Василеостровский</td>
      <td>Морской</td>
      <td>Голден Сити ЖК</td>
      <td>к1</td>
      <td>14 899 999 ₽</td>
      <td>275 620 ₽/м²</td>
      <td>https://spb.cian.ru/sale/flat/251938981/</td>
    </tr>
    <tr>
      <th>5535</th>
      <td>2-комн. кв., 94,6 м², 1/7 этаж</td>
      <td>ЖК «Futurist»</td>
      <td>Чкаловская</td>
      <td>12 минут пешком</td>
      <td>Санкт-Петербург</td>
      <td>р-н Петроградский</td>
      <td>Чкаловское</td>
      <td>Барочная улица</td>
      <td>4Ас2</td>
      <td>32 139 859 ₽</td>
      <td>339 745 ₽/м²</td>
      <td>https://spb.cian.ru/sale/flat/250578788/</td>
    </tr>
    <tr>
      <th>5536</th>
      <td>1-комн. кв., 45,3 м², 12/25 этаж</td>
      <td>ЖК «Шуваловский»</td>
      <td>Комендантский проспект</td>
      <td>5 минут на транспорте</td>
      <td>Санкт-Петербург</td>
      <td>р-н Приморский</td>
      <td>Коломяги</td>
      <td>улица Лидии Зверевой</td>
      <td>9к1</td>
      <td>6 155 000 ₽</td>
      <td>135 872 ₽/м²</td>
      <td>https://spb.cian.ru/sale/flat/258241964/</td>
    </tr>
    <tr>
      <th>5537</th>
      <td>2-комн. кв., 62,8 м², 8/25 этаж</td>
      <td>Беговая</td>
      <td>Беговая</td>
      <td>8 минут на транспорте</td>
      <td>Санкт-Петербург</td>
      <td>р-н Приморский</td>
      <td>№ 65</td>
      <td>улица Оптиков</td>
      <td>45к2</td>
      <td>11 250 000 ₽</td>
      <td>179 140 ₽/м²</td>
      <td>https://spb.cian.ru/sale/flat/251925639/</td>
    </tr>
  </tbody>
</table>
<p>5538 rows × 12 columns</p>
</div>




```python
df.to_csv('cian_advert_db.csv', encoding='utf-8', index=False)
```


```python
df = pd.read_csv('cian_advert_db.csv')
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Title</th>
      <th>Residential complex</th>
      <th>Nearest metro</th>
      <th>Remotnesses</th>
      <th>City</th>
      <th>District</th>
      <th>Region</th>
      <th>Street</th>
      <th>House num</th>
      <th>Full price</th>
      <th>Price for m2</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3-комн. кв., 85,3 м², 1/6 этаж</td>
      <td>ЖК «City Park»</td>
      <td>Деловой центр</td>
      <td>10 минут пешком</td>
      <td>Москва</td>
      <td>ЦАО</td>
      <td>р-н Пресненский</td>
      <td>Мантулинская улица</td>
      <td>9к6</td>
      <td>38 500 000 ₽</td>
      <td>451 348 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/251974435/</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3-комн. апарт., 113,3 м², 5/15 этаж</td>
      <td>ЖК «Hill8»</td>
      <td>Алексеевская</td>
      <td>4 минуты пешком</td>
      <td>Москва</td>
      <td>СВАО</td>
      <td>р-н Останкинский</td>
      <td>проспект Мира</td>
      <td>вл95</td>
      <td>39 810 455 ₽</td>
      <td>351 372 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/239980039/</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3-комн. апарт., 111,9 м², 9/10 этаж</td>
      <td>ЖК «Клубный дом Maison Rouge»</td>
      <td>Менделеевская</td>
      <td>2 минуты пешком</td>
      <td>Москва</td>
      <td>ЦАО</td>
      <td>р-н Тверской</td>
      <td>улица Палиха</td>
      <td>4</td>
      <td>74 525 400 ₽</td>
      <td>666 000 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/247916427/</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3-комн. апарт., 208,7 м², 8/8 этаж</td>
      <td>ЖК «LUMIN»</td>
      <td>Китай-город</td>
      <td>2 минуты пешком</td>
      <td>Москва</td>
      <td>ЦАО</td>
      <td>р-н Таганский</td>
      <td>Славянская площадь</td>
      <td>2/5/4с5</td>
      <td>260 875 000 ₽</td>
      <td>1 250 000 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/250364689/</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3-комн. апарт., 94 м², 2/20 этаж</td>
      <td>ЖК «Клубный дом SOHO+NOHO»</td>
      <td>Савеловская</td>
      <td>10 минут пешком</td>
      <td>Москва</td>
      <td>САО</td>
      <td>р-н Беговой</td>
      <td>Бумажный проезд</td>
      <td>4</td>
      <td>35 000 000 ₽</td>
      <td>372 340 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/260414438/</td>
    </tr>
  </tbody>
</table>
</div>




```python
google = 'китай-город'
indexes_match_queries = df.apply(
    lambda row: google in str(row['Nearest metro']).lower(),
    axis=1,
)
df[indexes_match_queries].sample(1)
#print(str(df[indexes_match_queries].sample(1)['Link']))
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Title</th>
      <th>Residential complex</th>
      <th>Nearest metro</th>
      <th>Remotnesses</th>
      <th>City</th>
      <th>District</th>
      <th>Region</th>
      <th>Street</th>
      <th>House num</th>
      <th>Full price</th>
      <th>Price for m2</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1313</th>
      <td>2-комн. апарт., 69,9 м², 6/8 этаж</td>
      <td>Китай-город</td>
      <td>Китай-город</td>
      <td>15 минут пешком</td>
      <td>Москва</td>
      <td>ЦАО</td>
      <td>р-н Таганский</td>
      <td>Серебрянический переулок</td>
      <td>4С1</td>
      <td>45 400 000 ₽</td>
      <td>649 499 ₽/м²</td>
      <td>https://www.cian.ru/sale/flat/259608832/</td>
    </tr>
  </tbody>
</table>
</div>




```python
google = 'китай-город'
indexes_match_queries = df.apply(
    lambda row: google in str(row['Nearest metro']).lower(),
    axis=1,
)
dl = df[indexes_match_queries].sample(1)
#print(dl)
print(str(dl['Link']))
```

    4756    https://www.cian.ru/sale/flat/250364689/
    Name: Link, dtype: object
    


```python
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
```

    4196    https://www.cian.ru/sale/flat/250364689/
    Name: Link, dtype: object
    


```python

```
