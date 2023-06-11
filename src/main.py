import requests
import pandas as pd
from bs4 import BeautifulSoup


def checking_page(s):
    # checking for the last page
    value = []
    all_page = s.find_all('a', class_='pagination-page')
    for p in all_page:
        value.append(p.text)
    if 'Последняя' in value:
        return True
    else:
        return False


def getting_data_from_ad(ind, ad):
    # getting data from each ad
    ad_id = str(page) + '.' + str(ind + 1)
    data[ad_id] = {}
    # find name
    name = ad.find('h3',
                   class_='title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH '
                          'text-text-LurtD text-size-s-BxGpL text-bold-SinUO').text
    # find url
    url = 'https://www.avito.ru' + ad.find('a', class_='iva-item-sliderLink-uLz1v').get('href')
    # find price
    price = ad.find('span', class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL').text
    # find address
    address = ad.find('div', class_='geo-root-zPwRk iva-item-geo-_Owyg').text
    # find date
    date = ad.find('div', class_='date-text-KmWDf text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs').text
    # adding data to the dictionary
    data[ad_id]['name'] = name
    data[ad_id]['url'] = url
    data[ad_id]['price'] = price.replace('\xa0', ' ')
    data[ad_id]['address'] = address.replace('\xa0', ' ')
    data[ad_id]['date'] = date


def processing_data(d):
    # do list from dictionary of data
    index = 0
    for key in d:
        data_list.append([key])
        data_list[index].append(d[key]['name'])
        data_list[index].append(d[key]['url'])
        data_list[index].append(d[key]['price'])
        data_list[index].append(d[key]['address'])
        data_list[index].append(d[key]['date'])
        index += 1
    return data_list


def sorting(s_t):
    # processing of sort type
    s_t = s_t.lower().strip()
    if s_t == 'по умолчанию':
        return ''
    elif s_t == 'сначала дешевле':
        return 1
    elif s_t == 'сначала дороже':
        return 2
    elif s_t == 'по дате':
        return 3


data = {}
string = input('Введите, интересующий Вас, товар\n')
string = string.replace(' ', '+')
sort_type = input('Введите тип сортировки. Доступные варианты:'
                  ' по умолчанию, сначала дешевле, сначала дороже, по дате\n')
sort_type_code = sorting(sort_type)
for page in range(1, 999):
    search = {'p': page, 'q': string, 's': sort_type_code}
    r = requests.get('https://www.avito.ru/ekaterinburg/', params=search)
    soup = BeautifulSoup(r.text, "html.parser")

    if checking_page(soup) is False:
        break

    ads = soup.find_all('div',
                        class_='iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH '
                               'iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih '
                               'items-listItem-Gd1jN js-catalog-item-enum')

    for i in range(len(ads)):
        getting_data_from_ad(i, ads[i])

data_list = []
processing_data(data)

csv_data = pd.DataFrame(data_list, columns=['page.number in order', 'name', 'url', 'price', 'address', 'date'])
filename = 'data.csv'
csv_data.to_csv(filename)
