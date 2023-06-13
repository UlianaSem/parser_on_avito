import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_soup_data(page, formatted_user_request, sort_type_code):
    """
    Делает запрос и возвращает объект BeautifulSoup
    :param page: номер страницы с объявлениями
    :param formatted_user_request: запрос для поиска
    :param sort_type_code: код типа сортировки
    :return: объект BeautifulSoup
    """
    search = {'p': page, 'q': formatted_user_request, 's': sort_type_code}

    r = requests.get('https://www.avito.ru/ekaterinburg/', params=search)
    soup = BeautifulSoup(r.text, "html.parser")

    return soup


def check_last_page(soup):
    """
    Проверяет последняя ли страница
    :param soup: объект BeautifulSoup
    :return: булевый тип
    """
    page_value = []
    all_page = soup.find_all('a', class_='pagination-page')

    for page in all_page:
        page_value.append(page.text)

    if 'Последняя' in page_value:
        return True
    else:
        return False


def get_data_from_ad(ad_data, index, ad, page):
    """
    Добавляет данные об объявлениях в словарь
    :param ad_data: словарь с данными об объявлениях
    :param index: индекс объявления
    :param ad: объявление
    :param page: номер страницы с объявлениями
    :return: словарь с данными об объявлениях
    """
    # getting data from each ad
    ad_id = str(page) + '.' + str(index + 1)
    ad_data[ad_id] = {}
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
    ad_data[ad_id]['name'] = name
    ad_data[ad_id]['url'] = url
    ad_data[ad_id]['price'] = price.replace('\xa0', ' ')
    ad_data[ad_id]['address'] = address.replace('\xa0', ' ')
    ad_data[ad_id]['date'] = date

    return ad_data


def get_processed_data(ads_data_to_processing):
    """
    Возвращает список из словаря с данными по объявлениям
    :param ads_data_to_processing: словарь с данными по объявлениям
    :return: список с данными по объявлениям
    """
    index = 0
    ads_processed_data = []

    for key in ads_data_to_processing:
        ads_processed_data.append([key])
        ads_processed_data[index].append(ads_data_to_processing[key]['name'])
        ads_processed_data[index].append(ads_data_to_processing[key]['url'])
        ads_processed_data[index].append(ads_data_to_processing[key]['price'])
        ads_processed_data[index].append(ads_data_to_processing[key]['address'])
        ads_processed_data[index].append(ads_data_to_processing[key]['date'])
        index += 1

    return ads_processed_data


def get_sorting_type(sort_type):
    """
    Возвращает код сортировки объявлений
    :param sort_type: тип сортировки
    :return: код сортировки
    """
    sort_type = sort_type.lower().strip()

    if sort_type == 'по умолчанию':
        return ''
    elif sort_type == 'сначала дешевле':
        return 1
    elif sort_type == 'сначала дороже':
        return 2
    elif sort_type == 'по дате':
        return 3


def save_to_csv(ads_data):
    """
    Создает csv-файл с данными по объявлениям
    :param ads_data: список с данными по объявлениям
    """
    csv_data = pd.DataFrame(ads_data, columns=['page.number in order', 'name', 'url', 'price', 'address', 'date'])
    filename = 'data.csv'
    csv_data.to_csv(filename)
