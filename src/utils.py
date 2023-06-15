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
    # получаем данные каждого объявления
    ad_id = str(page) + '.' + str(index + 1)
    ad_data[ad_id] = {}
    # находим название
    name = ad.find('h3',
                   class_='styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-'
                          'size_l-hruVE styles-module-ellipsis-LKWy3 styles-module-weight_bold-Kpd5F stylesMarningNorm'
                          'al-module-root-OSCNq stylesMarningNormal-module-header-l-qvNIS').text
    # находим url
    url = 'https://www.avito.ru' + ad.find('a', class_='iva-item-sliderLink-uLz1v').get('href')
    # находим цену
    price = ad.find('p', class_='styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l_dense-Wae_G '
                                'styles-module-size_l-hruVE styles-module-size_l_dense-xTg_p stylesMarningNormal-modul'
                                'e-root-OSCNq stylesMarningNormal-module-paragraph-l-dense-TTLmp').text
    # находим адрес
    address = ad.find('div', class_='geo-root-zPwRk').text
    # находим дату
    date = ad.find('p', class_='styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA stylesMa'
                               'rningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-s-_c6vD styles-modu'
                               'le-noAccent-nZxz7').text
    # добавляем данные в словарь
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
    Возвращает код сортировки объявлений, если тип сортировки введен неверно, то выбирается сортировка по умолчанию
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
    else:
        return ''


def save_to_csv(ads_data):
    """
    Создает csv-файл с данными по объявлениям
    :param ads_data: список с данными по объявлениям
    """
    csv_data = pd.DataFrame(ads_data, columns=['page.number in order', 'name', 'url', 'price', 'address', 'date'])
    filename = 'data.csv'
    csv_data.to_csv(filename)
